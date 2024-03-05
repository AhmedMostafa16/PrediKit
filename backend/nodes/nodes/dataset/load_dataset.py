from __future__ import annotations

import os
import pathlib
import sys
from typing import Tuple

import numpy as np
import pandas
from result import Ok, Result, Err
from sanic.log import logger
from nodes.properties.outputs.dataset_output import DatasetOutput

from nodes.properties.outputs.file_outputs import DatasetFileOutput
from nodes.utils.dataset_utils import get_available_dataset_formats

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import DatasetFileInput
from ...properties.outputs import TextOutput


@NodeFactory.register("predikit:dataset:load")
class DatasetReadNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Load dataset from specified file."
        self.inputs = [DatasetFileInput()]
        self.outputs = [
            DatasetOutput(label="Dataset"),
            TextOutput("Dataset Filename"),
        ]

        self.category = DatasetCategory
        self.name = "Load File"
        self.icon = "BsFileSpreadsheetFill"
        self.sub = "Input & Output"

    def run(self, path: str) -> tuple[pandas.DataFrame, str]:
        """Reads an dataset from the specified path and return it as a pandas DataFrame."""
        try:
            logger.debug(f"Reading dataset from path: {path}")
            directory = pathlib.Path(path)
            basename = directory.name.split(".")[0]
            ext = directory.suffix

            supported_formats = ext.lower() in get_available_dataset_formats()

            if not supported_formats:
                raise Exception(
                    f'The dataset "{path}" you are trying to read cannot be read by PrediKit.'
                )

            # Load the file
            try:
                df = pandas.DataFrame()
                match ext.lower():
                    case ".csv":
                        df = pandas.read_csv(path, engine="pyarrow")
                    case ".parquet":
                        df = pandas.read_parquet(path, engine="pyarrow")
                    case ".xlsx" | ".xls":
                        df = pandas.read_excel(path)
                    case ".json":
                        df = pandas.read_json(
                            path,
                        )
                    case ".feather":
                        df = pandas.read_feather(path, use_threads=True)
                    case _:
                        raise Exception(f"Unsupported file format: {ext}")

            except Exception as e:
                raise Exception(f"Error reading dataset: {e}")

            return df, basename
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
