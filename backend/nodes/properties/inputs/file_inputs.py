from __future__ import annotations

import os

# pylint: disable=relative-beyond-top-level
from ...utils.file_utils import get_available_dataset_formats
from .base_input import BaseInput
from .generic_inputs import DropDownInput


class FileInput(BaseInput):
    """Input for submitting a local file"""

    def __init__(
        self,
        input_type: str,
        label: str,
        filetypes: list[str],
        has_handle: bool = False,
    ):
        super().__init__(f"file::{input_type}", label, has_handle)
        self.filetypes = filetypes

    def toDict(self):
        return {
            **super().toDict(),
            "filetypes": self.filetypes,
        }

    def enforce(self, value):
        assert os.path.exists(value), f"{value} does not exist"
        # TODO: assert if the file exists on Azure Blob Storage instead of local file system
        return value


def DatasetFileInput() -> FileInput:
    """Input for submitting a local image file"""
    return FileInput(
        "image",
        "Image File",
        get_available_dataset_formats(),
        has_handle=False,
    )


def DirectoryInput(
    label: str = "Base Directory", has_handle: bool = False
) -> FileInput:
    """Input for submitting a local directory"""
    return FileInput("directory", label, ["directory"], has_handle)


def FileExtensionDropdown() -> DropDownInput:
    """Input for selecting file type from dropdown"""
    return DropDownInput(
        "File Extension",
        [
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
                "option": "Excel (XLS)",
                "value": "xls",
            },
            {
                "option": "Excel (XLSX)",
                "value": "xlsx",
            },
        ],
        input_type="image-extensions",
    )
