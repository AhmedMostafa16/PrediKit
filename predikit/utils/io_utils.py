"""
A utility module for handling file-related operations in Data Ingestion.
"""

import os
from enum import Enum
from io import BytesIO
from typing import Self


class FileExtension(Enum):
    """
    An enumeration of file extensions supported by PrediKit.
    This Enum is used to map file extensions to their corresponding
    pandas reader functions.
    """

    CSV = "csv"
    EXCEL = ("xlsx", "xls")
    JSON = "json"
    PICKLE = ("pkl", "p", "pickle")

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

        if isinstance(file, BytesIO):
            raise NotImplementedError(
                "This feature is not implemented yet. Currently you "
                "can only infer file extension from a file path."
            )

        return cls.from_file(file)
