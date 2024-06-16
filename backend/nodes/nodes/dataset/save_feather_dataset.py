from __future__ import annotations

import os
from typing import Literal, Union

from nodes.properties.inputs.generic_inputs import DropDownInput
from nodes.properties.inputs.file_inputs import DirectoryInput
from nodes.properties.inputs.dataset_input import DatasetInput
import pandas
from sanic.log import logger

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    TextInput,
)


@NodeFactory.register("predikit:dataset:save_feather")
class FeatherDatasetWriteNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = (
            "Save dataset to Feather file at a specified directory."
        )
        self.inputs = [
            DatasetInput(),
            DirectoryInput(has_handle=True),
            TextInput("Subdirectory Path").make_optional(),
            TextInput("File Name"),
            DropDownInput(
                input_type="string",
                label="Compression Algorithm",
                options=[
                    {"label": "None", "value": "uncompressed"},
                    {"label": "LZ4", "value": "lz4"},
                    {"label": "Zstd", "value": "zstd"},
                ],
            ),
        ]
        self.category = DatasetCategory
        self.name = "Save Feather Dataset"
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
        compression: Literal["lz4", "zstd", "uncompressed"],
    ):
        """Write a dataset to a file and return the file to the frontend"""

        # TODO: Pass file as a blob to the frontend

        full_file = f"{filename}.feather"
        logger.debug(f"Writing dataset to file: {full_file}")

        if relative_path and relative_path != ".":
            base_directory = os.path.join(base_directory, relative_path)
        full_path = os.path.join(base_directory, full_file)

        logger.debug(f"Writing dataset to path: {full_path}")

        os.makedirs(base_directory, exist_ok=True)

        try:
            pandas.DataFrame.to_feather(
                self=dataframe,
                path=full_path,
                compression=compression,
            )

        except Exception:
            raise ValueError(f"Failed to write dataset to path: {full_path}")
