import logging
import os
import sys
from typing import Any

import pandas as pd

root = os.path.dirname(os.path.abspath("../../predikit/"))
sys.path.append(root)
from workflow_state import WorkflowState

import predikit as pk
from predikit.util import export_index_correction


def execute_node(
    props: dict[str, Any], df: pd.DataFrame, node_type: str
) -> pd.DataFrame | None:
    VERBOSE = True
    logging.debug("entered execute_node")

    match node_type:
        case "inputDataNode":
            logging.debug("entered inputDataNode")

            ext: pk.FileExtension = pk.FileExtension.from_file(props["file"])
            df = pk.DataFrameParser(
                path_or_buf=props["file"],
                extension=ext,
                verbose=VERBOSE,
            )

            WorkflowState.original_file_extension = ext
            return df

        case "outputDataNode":
            logging.info("entered outputDataNode")
            logging.debug(
                f"Original Extension {WorkflowState.original_file_extension}"
            )

            ext = props["format"]

            if ext == "original":
                if WorkflowState.original_file_extension is None:
                    raise ValueError(
                        "Cannot infer file extension from original file."
                    )

                ext = WorkflowState.original_file_extension

            kwargs = {}
            if not ext == pk.FileExtension.PICKLE:
                kwargs = {
                    "index": export_index_correction(ext, props["indexColumn"])
                }

            dfe = pk.DataFrameExporter(
                df=df,
                extension=ext,
                filename=props["filename"],
                verbose=VERBOSE,
                **kwargs,
            )

            return dfe.export()

        case "dataCleansingNode":
            logging.debug("entered dataCleaningNode")

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
            ).fit_transform(df, columns=props["selectedColumns"])

            if result.is_err():
                return None

            return result.unwrap()

        case "basicFilterNode":
            logging.debug("entered basicFilterNode")
            result = pk.BasicFilteringProcessor(
                operator=props["operator"],
                value=props["value"],
                case_sensitive=props["caseSensitive"],
                verbose=VERBOSE,
            ).fit_transform(df, column=props["column"])

            if result.is_err():
                return None

            return result.unwrap()
