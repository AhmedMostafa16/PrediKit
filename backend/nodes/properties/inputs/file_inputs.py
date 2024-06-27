from __future__ import annotations

import os
from typing import (
    Literal,
    Union,
)

from .. import expression

# pylint: disable=relative-beyond-top-level
from ...utils.dataset_utils import get_available_dataset_formats
from ...utils.image_utils import get_available_image_formats
from .base_input import BaseInput
from .generic_inputs import DropDownInput

FileInputKind = Union[
    Literal["dataset"],
    Literal["bin"],
    Literal["image"],
    Literal["onnx"],
    Literal["param"],
    Literal["pt"],
    Literal["pth"],
]


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
        if not os.path.exists(value):
            raise AssertionError(f"File {value} does not exist")
        if not os.path.isfile(value):
            raise AssertionError(f"The path {value} is not a file")
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


def ImageFileInput() -> FileInput:
    """Input for submitting a local image file"""
    return FileInput(
        input_type="ImageFile",
        label="Image File",
        file_kind="image",
        filetypes=get_available_image_formats(),
        has_handle=False,
    )


def PthFileInput() -> FileInput:
    """Input for submitting a local .pth file"""
    return FileInput(
        input_type="PthFile",
        label="Pretrained Model",
        file_kind="pth",
        filetypes=[".pth"],
    )


def TorchFileInput() -> FileInput:
    """Input for submitting a local .pth or .pt file"""
    return FileInput(
        input_type="PtFile",
        label="Pretrained Model",
        file_kind="pt",
        filetypes=[".pt"],
    )


class DirectoryInput(BaseInput):
    """Input for submitting a local directory"""

    def __init__(
        self, label: str = "Base Directory", has_handle: bool = False
    ):
        super().__init__(
            "Directory", label, kind="directory", has_handle=has_handle
        )

    def enforce(self, value):
        if not os.path.exists(value):
            raise AssertionError(f"Directory {value} does not exist")
        return value


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


def ImageExtensionDropdown() -> DropDownInput:
    """Input for selecting file type from dropdown"""
    return DropDownInput(
        input_type="ImageExtension",
        label="Image Extension",
        options=[
            {
                "option": "PNG",
                "value": "png",
            },
            {
                "option": "JPG",
                "value": "jpg",
            },
            {
                "option": "GIF",
                "value": "gif",
            },
            {
                "option": "TIFF",
                "value": "tiff",
            },
            {
                "option": "WEBP",
                "value": "webp",
            },
            {
                "option": "TGA",
                "value": "tga",
            },
        ],
    )


def BinFileInput() -> FileInput:
    """Input for submitting a local .bin file"""
    return FileInput(
        input_type="NcnnBinFile",
        label="NCNN Bin File",
        file_kind="bin",
        filetypes=[".bin"],
    )


def ParamFileInput() -> FileInput:
    """Input for submitting a local .param file"""
    return FileInput(
        input_type="NcnnParamFile",
        label="NCNN Param File",
        file_kind="param",
        filetypes=[".param"],
    )


def OnnxFileInput() -> FileInput:
    """Input for submitting a local .onnx file"""
    return FileInput(
        input_type="OnnxFile",
        label="ONNX Model File",
        file_kind="onnx",
        filetypes=[".onnx"],
    )
