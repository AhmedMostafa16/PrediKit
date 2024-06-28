from __future__ import annotations

import gc
import os
import pathlib

import pandas
from sanic.log import logger

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import DatasetFileInput
from ...properties.outputs import TextOutput
from ...properties.outputs.dataset_output import DatasetOutput
from ...utils.dataset_utils import get_available_dataset_formats


@NodeFactory.register("predikit:dataset:load")
class DatasetReadNode(NodeBase):
    def __init__(self) -> None:
        super().__init__()
        self.description = "Load dataset from specified file."
        self.inputs = [DatasetFileInput()]
        self.outputs = [
            DatasetOutput(label="Dataset"),
            TextOutput("Dataset Filename"),
        ]

        self.category = DatasetCategory
        self.name = "Load File"
        self.icon = "MdUploadFile"
        self.sub = "Input"

    def run(self, path: str) -> tuple[pandas.DataFrame, str, str]:
        """Reads an dataset from the specified path and return it as a pandas DataFrame."""
        try:
            logger.debug(f"Reading dataset from path: {path}")
            _base, ext = os.path.splitext(path)

            supported_formats = ext.lower() in get_available_dataset_formats()

            if not supported_formats:
                raise Exception(
                    f'The dataset at path "{path}" cannot be read by PrediKit.'
                )

            # Load the file
            df: pandas.DataFrame

            try:
                match ext.lower():
                    case ".csv":
                        temp_df = tuple(
                            pandas.read_csv(path, header=None, nrows=5).dtypes
                        )
                        df_header = tuple(pandas.read_csv(path, nrows=5).dtypes)
                        has_header: bool = temp_df != df_header
                        df = pandas.read_csv(
                            filepath_or_buffer=path,
                            engine="pyarrow",
                            header=0 if has_header else None,
                        )
                    case ".xlsx" | ".xls":
                        temp_df = tuple(
                            pandas.read_excel(path, header=None, nrows=5).dtypes
                        )
                        df_header = tuple(pandas.read_excel(path, nrows=5).dtypes)
                        has_header: bool = temp_df != df_header
                        del temp_df, df_header
                        df = pandas.read_excel(
                            io=path,
                            header=0 if has_header else None,
                        )
                    case ".parquet":
                        df = pandas.read_parquet(path=path, engine="pyarrow")
                    case ".json":
                        df = pandas.read_json(
                            path_or_buf=path,
                        )
                    case ".feather":
                        df = pandas.read_feather(path=path, use_threads=True)
                    case ".pickle" | ".pkl" | ".pk":
                        df = pandas.read_pickle(filepath_or_buffer=path)
                    case _:
                        raise Exception(
                            f"Unsupported file format: {ext if ext != "" else path}"
                        )

                gc.collect()
            except Exception as e:
                raise Exception(f"Error reading dataset: {e}")
            dirname, basename = os.path.split(os.path.splitext(path)[0])
            return df, dirname, basename
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
