from __future__ import annotations

import os
from typing import Union

from nodes.properties.inputs.generic_inputs import BoolInput, DropDownInput
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


@NodeFactory.register("predikit:dataset:save_excel")
class ExcelDatasetWriteNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = (
            "Save dataset to Parquet file at a specified directory."
        )
        self.inputs = [
            DatasetInput(),
            DirectoryInput(has_handle=True),
            TextInput("Subdirectory Path").make_optional(),
            TextInput("File Name"),
            DropDownInput(
                input_type="string",
                label="Excel File Extension",
                options=[
                    {"label": "Excel Workbook (.xlsx)", "value": "xlsx"},
                    {"label": "Excel 97-2003 Workbook (.xls)", "value": "xls"},
                ],
            ),
            TextInput("Sheet Name").make_optional(),
            BoolInput("Save Header"),
        ]
        self.category = DatasetCategory
        self.name = "Save Excel Dataset"
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
        sheet_name: str,
        save_header: bool = True,
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
            pandas.DataFrame.to_excel(
                self=dataframe,
                excel_writer=full_path,
                sheet_name=sheet_name,
                header=save_header,
            )

        except Exception:
            raise ValueError(f"Failed to write dataset to path: {full_path}")
