import logging
import os
import sys
from typing import Any
import pandas as pd
from result import Ok, Result, Err
from redis_utils import redis_client

root = os.path.dirname(os.path.abspath("../../predikit/"))
sys.path.append(root)

import predikit as pk
from predikit.util import export_index_correction


def execute_node(
    props: dict[str, Any],
    dfs: list[pd.DataFrame],
    node_type: str,
    node_id: str,
) -> Result[None, str]:
    VERBOSE = False

    match node_type:
        case "inputDataNode":
            # logging.debug("entered inputDataNode")
            ext: pk.FileExtension = pk.FileExtension.from_file(props["file"])
            df = pk.DataFrameParser(
                path_or_buf=props["file"],
                extension=ext,
                verbose=VERBOSE,
            )
            logging.debug("Input Node: parsed dataframe")
            redis_client.cache_dataframe_in_redis(df, node_id)
            logging.debug("Input Node: cached dataframe in Redis")
            return Ok(None)

        case "outputDataNode":
            # logging.info("entered outputDataNode")

            ext = props["format"]

            kwargs = {}
            if not ext == pk.FileExtension.PICKLE:
                kwargs = {
                    "index": export_index_correction(ext, props["indexColumn"])
                }

            dfe = pk.DataFrameExporter(
                df=dfs[0],
                extension=ext,
                filename=props["filename"],
                verbose=VERBOSE,
                **kwargs,
            )

            dfe.export()

            return Ok(None)

        case "dataCleansingNode":
            # logging.debug("entered dataCleaningNode")

            result = pk.DataCleanser(
                missing_clean=props["missingClean"],
                missing_strategy=props["missingStrategy"],
                missing_fill_value=props["missingFillValue"],
                missing_indicator=props["missingIndicator"],
                outlier_clean=props["outlierClean"],
                outlier_method=props["outlierMethod"],
                outlier_threshold=props["outlierThreshold"],
                outlier_indicator=props["outlierIndicator"],
                str_operations=props["strOperations"],
                str_case_modifier_method=props["strCaseModifierMethod"],
                str_trim=props["strTrim"],
                str_remove_whitespace=props["strRemoveWhitespace"],
                str_remove_numbers=props["strRemoveNumbers"],
                str_remove_letters=props["strRemoveLetters"],
                str_remove_punctuation=props["strRemovePunctuation"],
                verbose=VERBOSE,
            ).fit_transform(dfs[0], columns=props["selectedColumns"])

            if result.is_err():
                return Err(result.unwrap_err())

            dataframe = result.unwrap()

            logging.debug(msg="Data Cleansing Node: parsed dataframe")
            redis_client.cache_dataframe_in_redis(dataframe, node_id)
            logging.debug("Data Cleansing Node: cached dataframe in Redis")

            return Ok(None)

        case "basicFilterNode":
            # logging.debug("entered basicFilterNode")
            result = pk.BasicFilteringProcessor(
                operator=props["operator"],
                value=props["value"],
                case_sensitive=props["caseSensitive"],
                verbose=VERBOSE,
            ).fit_transform(dfs[0], column=props["column"])

            if result.is_err():
                return Err(result.unwrap_err())

            dataframe = result.unwrap()

            logging.debug("Basic Filter Node: parsed dataframe")
            redis_client.cache_dataframe_in_redis(
                df=dataframe, key_prefix=node_id
            )
            logging.debug("Basic Filter Node: cached dataframe in Redis")

            return Ok(None)

        case "joinNode":
            return Err("Join node is not yet implemented")

    return Err("Invalid node type")
