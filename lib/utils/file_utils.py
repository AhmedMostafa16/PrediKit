from __future__ import annotations

import inspect
import os
from enum import Enum
from typing import Callable, TypeAlias

import pandas as pd

PdRead: TypeAlias = Callable[..., pd.DataFrame]


class FileUtils:
    """
    A utility class for working with files.
    """

    class Extension(Enum):
        """
        An enumeration of file extensions supported by PrediKit.
        """

        CSV = "csv"
        EXCEL = ("xlsx", "xls")
        JSON = "json"
        PICKLE = ("pkl", "p", "pickle")

        @staticmethod
        def from_string(extension: str) -> FileUtils.Extension:
            for ext in FileUtils.Extension:
                if isinstance(ext.value, tuple) and extension in ext.value:
                    return ext

                if extension == ext.value:
                    return ext

            raise ValueError

    READERS: dict[Extension, PdRead] = {
        Extension.CSV: pd.read_csv,
        Extension.EXCEL: pd.read_excel,
        Extension.JSON: pd.read_json,
        Extension.PICKLE: pd.read_pickle,
    }

    @staticmethod
    def get_extension(file: str) -> Extension:
        """
        Returns the extension of a file.

        Args:
            file (str): The file path.

        Returns:
            str: The extension of the file.
        """
        _, ext = os.path.splitext(file)
        return FileUtils.Extension.from_string(ext.lstrip(".").lower())

    @staticmethod
    def is_type_of(extension: str, criteria: list[str]) -> bool:
        """
        Check if the given extension is of the specified criteria.

        Args:
            extension (str): The extension to check.
            criteria (list[str]): The list of criteria to check against.

        Returns:
            bool: True if the extension is of the specified criteria, False otherwise.
        """
        return extension in criteria

    @staticmethod
    def get_reader(ext: Extension) -> PdRead:
        """
        Returns a callable that can read a file with the given extension and return its contents as a pandas DataFrame.

        Args:
            ext (Extension): The file extension to read.

        Returns:
            Callable[..., pd.DataFrame]: A callable that can read a file with the given extension and return its contents as a pandas DataFrame.
        """
        return FileUtils.READERS[ext]

    @staticmethod
    def get_properties(reader: PdRead):
        """
        Get the possible properties of a Pandas reader object.
        Useful for Views module when viewing each Node property,
        with their default value, other possible values and
        data types to validate against user selection.

        Args:
            reader (PdRead): A Pandas reader object.

        Returns:
            dict: A dictionary containing the possible properties of the reader object.
        """
        params = inspect.signature(reader).parameters
        possible_properties = {}
        for name, param in params.items():
            param_default = param.default
            param_dtype = param.annotation

            if param_default is inspect.Parameter.empty:
                param_default = None

            if param_dtype is inspect.Parameter.empty:
                param_dtype = None

            possible_properties[name] = {param_default, param_dtype}

        return possible_properties
