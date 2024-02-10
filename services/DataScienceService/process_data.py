import logging
from typing import Dict
import pandas
from redis_utils import get_all_chunks, redis_client
import executor


async def process_data(props: Dict) -> bytes:
    """
    Process the data based on the provided properties.

    Args:
        props (Dict): A dictionary containing the properties for data processing.

    Returns:
        bytes: The result of the data processing as bytes.

    Raises:
        Exception: If an error occurs during data processing.
    """
    dfs: list[pandas.DataFrame] = []
    logging.debug("Processing data")
    # logging.debug("Props: " + props) # type: ignore
    dependencies: list[str] = props.get("Dependencies", [])
    if dependencies:
        logging.debug(msg="Dependencies: " + str(dependencies))
        # Check if Redis has the result of the previous node
        # If it does, use that as the input
        # If it doesn't, execute the previous node then wait for the result of the previous node
        for dep in dependencies:
            df = await get_all_chunks(redis_client, dep)
            logging.debug("Got Dataframe with name: " + dep + " from Redis")
            if df is not None:
                logging.debug("Dataframe is not None")
                dfs.append(df)
            else:
                msg = "The dependency nodes are not found in the cache, please execute the previous nodes first"
                logging.debug(msg)
                return msg.encode("ascii")
                # TODO: Execute the dependency nodes then wait for the result of the execution

    else:
        logging.debug("No dependency nodes")
        dfs.append(pandas.DataFrame())

    try:
        logging.debug("Executing node")
        result = await executor.execute_node(
            props=props["Data"],
            dfs=dfs,
            node_type=props["NodeType"],
            node_id=props["CurrentId"],
        )
    except Exception as e:
        logging.error(e)
        return str(e).encode("ascii")

    logging.debug("Result: " + str(True if result.is_ok() else False))

    if result.is_ok():
        return b"Ok"
    else:
        return result.unwrap_err().encode("ascii")
