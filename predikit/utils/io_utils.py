"""
A utility module for handling file-related operations in Data Ingestion.
"""

from enum import Enum
from io import BytesIO
import os
from typing import Self


class FileExtension(Enum):
    """
    An enumeration of file extensions supported by PrediKit.
    This Enum is used to map file extensions to their corresponding
    pandas reader functions.
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    EXCEL = ("xlsx", "xls")
    PICKLE = ("pickle", "p", "pkl")

    @classmethod
    def _correct_string(cls, extension: str):
        return extension.lstrip(".").lower()

    @classmethod
    def from_string(cls, extension: str) -> Self:
        """
        Converts a string to a FileExtension enum member.

        Parameters
        ----------
        extension : str
            The file extension as a string.

        Returns
        -------
        FileExtension
            The corresponding FileExtension enum member.

        Raises
        ------
        ValueError
            If the string does not match any FileExtension enum member.
        """
        extension = cls._correct_string(extension)
        for ext in cls:
            if isinstance(ext.value, tuple) and extension in ext.value:
                return ext

            if extension == ext.value:
                return ext

        supported_extensions = ", ".join(
            [
                ext.value
                if isinstance(ext.value, str)
                else ", ".join(ext.value)
                for ext in cls
            ]
        )

        raise ValueError(
            "Unsupported file extension: {0}. "
            "Supported extensions are: {1}".format(
                extension, supported_extensions
            )
        )

    @classmethod
    def from_file(cls, file: str | os.PathLike) -> Self:
        """
        Determines the extension of a file.

        Parameters
        ----------
        file : os.PathLike
            The file path.

        Returns
        -------
        FileExtension
            The corresponding FileExtension enum member.
        """
        _, ext = os.path.splitext(file)
        return cls.from_string(ext.lstrip(".").lower())

    @classmethod
    def parse(
        cls,
        *,
        extension: Self | str | None = None,
        file: str | os.PathLike | BytesIO,
    ) -> Self:
        """
        Parses the file extension from a string or file.

        Parameters
        ----------
        extension : Self | str | None, optional
            The file extension as a string or a member of the FileExtension
            Enum. If None, the extension is inferred from the file.
        file : os.PathLike | BytesIO
            The file from which to infer the extension.

        Returns
        -------
        Self
            A member of the Enum representing the file extension.

        Raises
        ------
        NotImplementedError
            If the file is a BytesIO object, from which the extension
            cannot be inferred.
        """
        if extension:
            if isinstance(extension, str):
                return cls.from_string(extension)
            if isinstance(extension, cls):
                return extension

        if not file:
            raise ValueError(
                "Either the extension or the file must be specified."
            )

        # no need to implement this since we get the dataset as BytesIO
        # associated with its extensions from the frontend.
        if isinstance(file, BytesIO):
            raise NotImplementedError(
                "This feature is not implemented yet. Currently you "
                "can only infer file extension from a file path."
            )

        return cls.from_file(file)


def ext_to_str(ext: FileExtension) -> str:
    return (
        f".{ext.value}" if not isinstance(ext, tuple) else f".{ext.value[0]}"
    )


def get_home() -> str:
    return os.path.expanduser("~")


def append_to_home(file: str) -> str:
    return os.path.join(get_home(), file)


def abs_path(dir: str, file: str) -> str:
    return os.path.join(dir, file)


def init_dir(name: str) -> None:
    os.makedirs(name, exist_ok=True)
