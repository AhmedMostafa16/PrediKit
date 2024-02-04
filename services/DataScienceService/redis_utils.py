import redis

# Global Redis client
import logging
import pandas as pd

# import redis
import redis.asyncio as redis
from io import BytesIO

redis_pool = redis.ConnectionPool(host='localhost', port=6377, db=0)
redis_client = redis.StrictRedis(
    connection_pool=redis_pool
)

CHUNK_SIZE = 1000


async def cache_dataframe_in_redis(
    df: pd.DataFrame, redis_client: redis.Redis, key_prefix: str
):
    """
    Caches a DataFrame in Redis by splitting it into chunks and storing each chunk as a separate key-value pair.

    Args:
        df (pd.DataFrame): The DataFrame to be cached in Redis.
        redis_client (redis.Redis): The Redis client object.
        key_prefix (str): The prefix to be added to the Redis keys.

    Returns:
        None
    """
    total_rows: int = len(df.index)
    num_chunks: int = (total_rows // CHUNK_SIZE) + 1

    await delete_all_chunks(redis_client, key_prefix)

    async with redis_client.pipeline() as pipe:
        for i in range(num_chunks):
            offset: int = i * CHUNK_SIZE
            # Create a chunk of the PySpark DataFrame
            # chunk_df = (
            #     df.limit(chunk_size)
            #     .filter(f"row_number() > {offset}")
            #     .filter(f"row_number() <= {offset + chunk_size}")
            # )

            # Create a chunk of the Pandas DataFrame
            chunk_df = df.iloc[offset : offset + CHUNK_SIZE]

            # Cache the Pandas DataFrame in Redis
            redis_key: str = f"{key_prefix}_{i}"
            pipe.set(redis_key, chunk_df.to_parquet(engine="pyarrow"))

        await pipe.execute()


async def get_cached_data_chunk(
    redis_client: redis.Redis, key_prefix: str, page_number: int
) -> pd.DataFrame | None:
    """
    Retrieves a cached data chunk from a Redis server and returns it as a Pandas DataFrame.

    Args:
        redis_client: A Redis client object used to connect to the Redis server.
        key_prefix: A string representing the prefix of the Redis key for the cached data chunk.
        page_number: An integer representing the page number of the cached data chunk.

    Returns:
        A Pandas DataFrame containing the cached data chunk, or None if the data is not found or an error occurs.
    """
    redis_key = f"{key_prefix}_{page_number}"
    try:
        serialized_data = await redis_client.get(redis_key)
        if serialized_data is not None:
            return pd.read_parquet(BytesIO(serialized_data), engine="pyarrow")
    except Exception as e:
        logging.error(e)

    return None


async def get_all_chunks(
    redis_client: redis.Redis, key_prefix: str
) -> pd.DataFrame:
    """
    Retrieve all data chunks from Redis with the given key prefix and return them as a single pandas DataFrame.

    Parameters:
        redis_client (redis.Redis): The Redis client object.
        key_prefix (str): The prefix of the keys to search for in Redis.

    Returns:
        pd.DataFrame: The concatenated DataFrame containing all the data chunks.

    """
    keys = redis_client.scan_iter(match=key_prefix + "_*")
    dataframes = []
    # Use pipeline for better performance
    async for key in keys:
        data = await redis_client.get(key)
        dataframes.append(pd.read_parquet(BytesIO(initial_bytes=data), engine="pyarrow"))  # type: ignore

    return pd.concat(dataframes)


async def delete_all_chunks(redis_client: redis.Redis, key_prefix: str):
    """
    Delete all chunks with the given key prefix from Redis.

    Args:
        redis_client (redis.Redis): The Redis client.
        key_prefix (str): The prefix of the keys to delete.

    Returns:
        None
    """
    keys = redis_client.scan_iter(match=key_prefix + "_*")

    async with redis_client.pipeline() as pipe:
        async for key in keys:
            await pipe.delete(key)

        await pipe.execute()
