"""
Auto parser for buffers or files into pandas DataFrames.
"""
from io import BytesIO
from os import PathLike
from typing import (
    Any,
    Callable,
)

import numpy as np
from pandas import (
    DataFrame,
    read_csv,
    read_excel,
    read_json,
    read_parquet,
    read_pickle,
)

from predikit._typing import (
    FilePath,
    PdReader,
)
from predikit.utils import (
    FileExtension,
    validations,
)


class DataFrameParser(DataFrame):
    """
    DataFrameParser is a subclass of pandas DataFrame that provides
    additional functionality for automatically parsing various file
    types into pandas DataFrames.

    The class supports parsing from CSV, JSON, Parquet, Excel, and Pickle files.
    It also provides the ability to ignore invalid properties when loading
    data, and to inspect the properties of pandas reader functions.

    Parameters
    ----------
    path_or_buf : str, os.PathLike, BytesIO, dict, np.ndarray, or list
        The file or buffer to be parsed. If it's a file, the path to the file
        is expected.
    extension : FileExtension, str, or None, optional
        The file extension. If None, it will be inferred from the file.
    ignore_wrong_properties : bool, optional
        If True, properties that are not valid for the pandas reader function
        will be ignored.
    properties : dict, optional
        Additional properties to pass to the pandas reader function.

    Attributes
    ----------
    _ignore : bool
        If True, properties that are not valid for the pandas reader function
        will be ignored.
    _READERS : dict
        A mapping from file extensions to pandas reader functions.
    """

    _metadata = ["_ignore"]

    _READERS: dict[FileExtension, PdReader] = {
        FileExtension.CSV: read_csv,
        FileExtension.JSON: read_json,
        FileExtension.PARQUET: read_parquet,
        FileExtension.EXCEL: read_excel,
        FileExtension.PICKLE: read_pickle,
    }

    def __init__(
        self,
        path_or_buf: FilePath | BytesIO | dict | np.ndarray | list,
        *,
        extension: FileExtension | str | None = None,
        ignore_wrong_properties: bool = False,
        **properties,
    ) -> None:
        self._ignore = ignore_wrong_properties
        data = self._load(path_or_buf, extension, **properties)
        super(DataFrameParser, self).__init__(data)  # type: ignore

    def _get_reader(self, extension: FileExtension) -> PdReader:
        """
        Returns the appropriate pandas reader function based on the
        file extension.

        Parameters
        ----------
        extension : FileExtension
            The file extension for which to get the reader function.

        Returns
        -------
        PdReader
            The pandas reader function for the specified file extension.

        Raises
        ------
        TypeError
            If there is no reader function for the specified file extension.
        """
        reader = self._READERS.get(extension)
        if not reader:
            raise TypeError(f"No reader for type {extension}")
        return reader

    def _load(
        self,
        path_or_buf: FilePath | BytesIO | dict | np.ndarray | list,
        extension: FileExtension | str | None,
        **properties,
    ) -> DataFrame:
        """
        Loads a DataFrame from a file, a BytesIO stream, or a buffer.

        This method determines the type of the input, then uses the
        appropriate loader function to load the DataFrame. If the input
        is a file or a BytesIO stream, it also parses the file extension.

        Parameters
        ----------
        path_or_buf : FilePath | BytesIO | dict | np.ndarray | list
            The path to the file, a BytesIO stream, or a buffer to
            load into a DataFrame.
        extension : FileExtension | str | None
            The file extension of the file to load. This is ignored if the
            input is a buffer.
        **properties : dict
            Additional properties to pass to the loader function.

        Returns
        -------
        DataFrame
            The loaded DataFrame.

        Raises
        ------
        TypeError
            If the type of the input is not supported.
        """
        df: DataFrame

        if isinstance(path_or_buf, (np.ndarray, dict, list)):
            df = self._buf_loader(path_or_buf, **properties)

        elif isinstance(path_or_buf, (str, PathLike, BytesIO)):
            extension = FileExtension.parse(
                extension=extension, file=path_or_buf
            )
            df = self._file_loader(path_or_buf, extension, **properties)

        else:
            raise TypeError(
                "Unsupported type ({}) for path_or_buf. Supported "
                "types are (str, os.PathLike, BytesIO, dict, "
                "np.ndarray).".format(type(path_or_buf))
            )

        return df

    def _buf_loader(
        self, buf: np.ndarray | dict | list, **properties
    ) -> DataFrame:
        """
        Loads a DataFrame from a buffer.

        This method checks and fixes properties if `_ignore` is False, then
        initializes a DataFrame with the buffer and properties.

        Parameters
        ----------
        buf : np.ndarray | dict | list
            The buffer to load into a DataFrame. This can be a NumPy array,
            a dictionary, or a list.
        **properties : dict
            Additional properties to pass to the DataFrame constructor.

        Returns
        -------
        DataFrame
            The loaded DataFrame.
        """
        if not self._ignore:
            properties = self.__check_fix_properties(
                func=DataFrame.__init__, **properties
            )
        return DataFrame(buf, **properties)

    def _file_loader(
        self,
        path: FilePath | BytesIO,
        extension: FileExtension,
        **properties,
    ) -> DataFrame:
        """
        Loads a DataFrame from a file or a BytesIO stream.

        This method gets the appropriate reader function based on the file
        extension, checks and fixes properties if `_ignore` is False, then
        uses the reader function to load the DataFrame from the file or stream.

        Parameters
        ----------
        path : FilePath | BytesIO
            The path to the file or a BytesIO stream to load into a DataFrame.
        extension : FileExtension
            The file extension of the file to load.
        **properties : dict
            Additional properties to pass to the reader function.

        Returns
        -------
        DataFrame
            The loaded DataFrame.
        """
        reader = self._get_reader(extension)
        if not self._ignore:
            properties = self.__check_fix_properties(func=reader, **properties)

        return reader(path, **properties)

    def __check_fix_properties(
        self, func: Callable[..., Any], **kwargs
    ) -> dict:
        """
        Validate Keyword argument of a function (key/name only) value checker
        is not supported yet.


        Parameters
        ----------
        func : Callable[..., Any]
            The function to retrieve its parameters and validate
            properties against.

        Returns
        -------
        dict
            Empty properties if there's a single invalid keyword argument
        """
        valid_prop = validations.validate_reader_kwargs(func, kwargs)
        props = {} if not valid_prop else kwargs
        return props
