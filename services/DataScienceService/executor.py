import logging
import os
import sys
from typing import Any

import pandas as pd

root = os.path.dirname(os.path.abspath("../../predikit/"))
sys.path.append(root)
import predikit as pk


def execute_node(props: Any, df: pd.DataFrame, node_type: str) -> pd.DataFrame | None:
    logging.info("entered execute_node")
    # logging.info("df: ", df)
    # logging.info("node_type: ", node_type)
    print("entered execute_node")
    match node_type:
        case "inputDataNode":
            logging.info("entered inputDataNode")
            result = pk.DataFrameParser(
                path_or_buf=props['file'], extension=props["extension"])
            return result
        case "outputDataNode":
            logging.info("entered outputDataNode")
            print("props: ", props)
            result = pk.DataFrameExporter(df=df, extension=pk.FileExtension(
                str(props["format"])), filename=props["filename"])
            result.export()
            return None
        case "dataCleansingNode":
            logging.info("entered dataCleaningNode")
            print("props: ", props)
            result = pk.DataCleanser(  # TODO: add more options
                missing_clean=props["replaceNulls"],
                missing_strategy=pk.MissingValueStrategy(
                    props["replaceNullWith"]),
                missing_fill_value=props["fillValue"],
                outlier_clean=props["removeOutliers"],
                outlier_method=pk.OutlierDetectionMethod(
                    props["outlierMethod"]),
                str_remove_letters=props["removeLetters"],
                str_remove_numbers=props["removeNumbers"],
                str_remove_punctuation=props["removePunctuation"],
                str_remove_whitespace=props["removeWhitespace"],
                str_case_modifier_method=pk.CaseModifyingMethod.from_str(
                    props["modifyCase"]),
                str_trim=props["trim"],
                str_operations=True,
                outlier_indicator=True,
                verbose=True
            ).fit_transform(df, columns=props["selectedColumns"])

            if result.is_err():
                return None

            return result.unwrap()
        case "basicFilterNode":
            logging.info("entered basicFilterNode")
            bfp = pk.BasicFilteringProcessor(
                operator=pk.FilterOperator(props["operator"]),
                value=props["value"],
                case_sensitive=props["caseSensitive"],
            )

            result = bfp.fit_transform(df, column=props["column"])
            return result
            # return output
