from __future__ import annotations

import os
import sys

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

root = os.path.dirname(os.path.abspath("../../../../predikit/"))
sys.path.append(root)

from predikit import (
    DataFrameExporter,
    FileExtension,
)


@NodeFactory.register("predikit:dataset:save")
class DatasetWriteNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Save dataset to file at a specified directory."
        self.inputs = [
            DatasetInput(),
            TextInput("File Name"),
            DatasetExtensionDropdown(),
        ]
        self.category = DatasetCategory
        self.name = "Save Dataset"
        self.outputs = []
        self.icon = "MdSave"
        self.sub = "Input & Output"

        self.side_effects = True

    def run(
        self,
        dataframe: pandas.DataFrame,
        file_name: str,
        extension: str,
    ):
        """Write a dataset to a file and return the file to the frontend"""

        # TODO: Pass file as a blob to the frontend

        full_file = f"{file_name}.{extension}"
        logger.debug(f"Writing dataset to file: {full_file}")

        file = DataFrameExporter(
            filename=file_name,
            df=dataframe,
            extension=FileExtension(extension),
        ).export()
