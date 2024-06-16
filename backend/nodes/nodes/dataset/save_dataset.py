# ruff: noqa: E402

from __future__ import annotations

import os
from typing import Union

from nodes.properties.inputs.file_inputs import DirectoryInput
from nodes.properties.inputs.dataset_input import DatasetInput
import pandas
from sanic.log import logger

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    DatasetExtensionDropdown,
    TextInput,
)


@NodeFactory.register("predikit:dataset:save")
class DatasetGenericWriteNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Save dataset to file at a specified directory. It provides generic options for saving a dataset."
        self.inputs = [
            DatasetInput(),
            DirectoryInput(has_handle=True),
            TextInput("Subdirectory Path").make_optional(),
            TextInput("File Name"),
            DatasetExtensionDropdown(),
        ]
        self.category = DatasetCategory
        self.name = "Generic Save Dataset"
        self.outputs = []
        self.icon = "MdSave"
        self.sub = "Output"

        self.side_effects = True

    def run(
        self,
        dataframe: pandas.DataFrame,
        base_directory: str,
        relative_path: Union[str, None],
        filename: str,
        extension: str,
    ):
        """Write a dataset to a file and return the file to the frontend"""

        # TODO: Pass file as a blob to the frontend

        full_file = f"{filename}.{extension}"
        logger.debug(f"Writing dataset to file: {full_file}")

        if relative_path and relative_path != ".":
            base_directory = os.path.join(base_directory, relative_path)
        full_path = os.path.join(base_directory, full_file)

        logger.debug(f"Writing dataset to path: {full_path}")

        os.makedirs(base_directory, exist_ok=True)

        try:
            match extension.lower():
                case "csv":
                    pandas.DataFrame.to_csv(dataframe, full_path)
                case "parquet":
                    pandas.DataFrame.to_parquet(dataframe, full_path)
                case "xlsx":
                    pandas.DataFrame.to_excel(dataframe, full_path)
                case "xls":
                    pandas.DataFrame.to_excel(dataframe, full_path)
                case "json":
                    pandas.DataFrame.to_json(dataframe, full_path)
                case "feather":
                    pandas.DataFrame.to_feather(dataframe, full_path)
                case "pickle" | "pkl" | "pk":
                    pandas.DataFrame.to_pickle(dataframe, full_path)
                case _:
                    raise ValueError(
                        f"Unsupported dataset format: {extension}"
                    )
        except Exception:
            raise ValueError(f"Failed to write dataset to path: {full_path}")
