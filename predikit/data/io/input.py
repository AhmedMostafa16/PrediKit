"""
Auto detect file type and parse it into a pandas DataFrame.
"""
import inspect
import os
from io import BytesIO
from typing import Any
from typing import Callable

import pandas as pd

from ...utils import FileExtension
from ...utils.validations import Validations

type PdReader = Callable[..., pd.DataFrame]


class DataFrameParser(object):
    """
    A class used to parse different file types into pandas DataFrames.

    Attributes
    ----------
    file : os.PathLike | BytesIO
        The file to be parsed.
    extension : str | None
        The file extension. If None, it will be inferred from the file.
    properties : dict[str, Any]
        Additional properties to pass to the pandas reader function.
    """

    _READERS: dict[FileExtension, PdReader] = {
        FileExtension.CSV: pd.read_csv,
        FileExtension.JSON: pd.read_json,
        FileExtension.PARQUET: pd.read_parquet,
        FileExtension.EXCEL: pd.read_excel,
        FileExtension.PICKLE: pd.read_pickle,
    }

    def __init__(
        self,
        file: str | os.PathLike | BytesIO,
        *,
        extension: FileExtension | str | None = None,
        **properties: Any,
    ) -> None:
        self.file = file

        self.extension = FileExtension.parse(extension=extension, file=file)

        self.properties = properties

    def get_reader(self) -> PdReader:
        """
        Returns the appropriate pandas reader function based on the file extension.
        """
        return self._READERS[self.extension]

    def get_properties(self) -> dict[str, set[str | type] | None]:
        """
        Get the possible properties of a Pandas reader object.

        Notes
        -----
        Useful for Views module when viewing each Node property, with their
        default value, other possible values and data types to validate
        against user selection.

        Returns
        -------
        dict
            A dictionary containing the possible properties of the reader object.
        """
        reader = self.get_reader()

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

    def load(self) -> pd.DataFrame:
        """
        Load a file as a pandas DataFrame.

        Returns
        -------
        res.Result
            A Result object containing either a pandas DataFrame
            or an error message.
        """

        reader = self.get_reader()
        valid_prop = Validations.validate_reader_kwargs(reader, self.properties)
        props = {} if not valid_prop else self.properties

        df = reader(self.file, **props)
        return df
