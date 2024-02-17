import threading
import redis

# Global Redis client
import logging
import pandas as pd

from io import BytesIO

CHUNK_SIZE = 1000


class RedisClient:
    _instance = None
    _lock = threading.Lock()
    _connection_pool = None

    def __new__(cls) -> "RedisClient":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connection_pool = redis.ConnectionPool(
                    host="localhost", # Use the default host for now
                    port=6377, # Use a custom port for now
                    db=0,  # Use the default database for now
                )
        return cls._instance

    def get_connection(self) -> redis.StrictRedis:
        return redis.StrictRedis(connection_pool=self._connection_pool)

    def cache_dataframe_in_redis(self, df: pd.DataFrame, key_prefix: str):
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

        self.delete_all_chunks(key_prefix)

        with self.get_connection() as conn:
            with conn.pipeline() as pipe:
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

                pipe.execute()

    def get_cached_data_chunk(
        self, key_prefix: str, page_number: int
    ) -> pd.DataFrame | None:
        """
        Retrieves a cached data chunk from a Redis server and returns it as a Pandas DataFrame.

        Args:
            key_prefix: A string representing the prefix of the Redis key for the cached data chunk.
            page_number: An integer representing the page number of the cached data chunk.

        Returns:
            A Pandas DataFrame containing the cached data chunk, or None if the data is not found or an error occurs.
        """
        redis_key = f"{key_prefix}_{page_number}"
        with self.get_connection() as conn:
            try:
                serialized_data = conn.get(redis_key)
                if serialized_data is not None:
                    return pd.read_parquet(BytesIO(serialized_data), engine="pyarrow")  # type: ignore
            except Exception as e:
                logging.error(e)

        return None

    def get_all_chunks(self, key_prefix: str) -> pd.DataFrame:
        """
        Retrieve all data chunks from Redis with the given key prefix and return them as a single pandas DataFrame.

        Parameters:
            key_prefix (str): The prefix of the keys to search for in Redis.

        Returns:
            pd.DataFrame: The concatenated DataFrame containing all the data chunks.

        """
        with self.get_connection() as conn:
            keys = conn.scan_iter(match=key_prefix + "_*")
            dataframes = []
            try:
                for key in keys:
                    data = conn.get(key)
                    parsed_df = pd.read_parquet(
                        BytesIO(initial_bytes=data), engine="pyarrow"  # type: ignore
                    )
                    dataframes.append(parsed_df)
                return pd.concat(dataframes) if dataframes else pd.DataFrame()
            except Exception as e:
                logging.error(e)
                return pd.DataFrame()

    def delete_all_chunks(self, key_prefix: str):
        """
        Delete all chunks with the given key prefix from Redis.

        Args:
            key_prefix (str): The prefix of the keys to delete.

        Returns:
            None
        """
        with self.get_connection() as conn:
            keys = conn.scan_iter(match=key_prefix + "_*")

            with conn.pipeline() as pipe:
                for key in keys:
                    pipe.delete(key)

                pipe.execute()


redis_client = RedisClient()
