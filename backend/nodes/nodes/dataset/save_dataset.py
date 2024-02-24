from __future__ import annotations
from ast import match_case

import os
import random
import string
import sys
from typing import Union
import pandas
from result import Ok

from sanic.log import logger

from nodes.properties.inputs.dataset_input import DatasetInput

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    TextInput,
    DatasetExtensionDropdown,
)


root = os.path.dirname(os.path.abspath("../../../../predikit/"))
sys.path.append(root)

from predikit import FileExtension, DataFrameExporter


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
        filename: str,
        extension: str,
    ):
        """Write a dataset to a file and return the file to the frontend"""

        # TODO

        full_file = f"{filename}.{extension}"
        logger.debug(f"Writing dataset to file: {full_file}")

        file = DataFrameExporter(
            dataframe, extension=FileExtension(extension)
        ).export()

        return Ok(full_file)
