from __future__ import annotations

import os
from typing import (
    Literal,
    Union,
)

from .. import expression

# pylint: disable=relative-beyond-top-level
from ...utils.dataset_utils import get_available_dataset_formats
from .base_input import BaseInput
from .generic_inputs import DropDownInput

FileInputKind = Literal["dataset"]  # later it will be a Union


class FileInput(BaseInput):
    """Input for submitting a local file"""

    def __init__(
        self,
        input_type: expression.ExpressionJson,
        label: str,
        file_kind: FileInputKind,
        filetypes: list[str],
        has_handle: bool = False,
    ):
        super().__init__(input_type, label, kind="file", has_handle=has_handle)
        self.filetypes = filetypes
        self.file_kind = file_kind

    def toDict(self):
        return {
            **super().toDict(),
            "filetypes": self.filetypes,
            "fileKind": self.file_kind,
        }

    def enforce(self, value) -> str:
        assert isinstance(value, str)
        assert os.path.exists(value), f"File {value} does not exist"
        assert os.path.isfile(value), f"The path {value} is not a file"
        return value


def DatasetFileInput() -> FileInput:
    """Input for submitting a local dataset file"""
    return FileInput(
        input_type="DatasetFile",
        label="Dataset File",
        file_kind="dataset",
        filetypes=get_available_dataset_formats(),
        has_handle=False,
    )


def DatasetExtensionDropdown() -> DropDownInput:
    """Input for selecting file type from dropdown"""
    return DropDownInput(
        input_type="string",
        label="Dataset Extension",
        options=[
            {
                "option": "CSV",
                "value": "csv",
            },
            {
                "option": "JSON",
                "value": "json",
            },
            {
                "option": "Parquet",
                "value": "parquet",
            },
            {
                "option": "Feather",
                "value": "feather",
            },
            {
                "option": "HDF5",
                "value": "hdf5",
            },
            {
                "option": "Pickle",
                "value": "pickle",
            },
            {
                "option": "XLS",
                "value": "xls",
            },
            {
                "option": "XLSX",
                "value": "xlsx",
            },
        ],
    )
