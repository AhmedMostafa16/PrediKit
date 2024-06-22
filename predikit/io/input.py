"""
Auto parser for buffers or files into pandas DataFrames.
"""

from io import BytesIO
import logging
from os import PathLike
from typing import (
    Any,
    Callable,
    LiteralString,
    Self,
    cast,
    # override,
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
from predikit.util import (
    FileExtension,
    file_exists,
    get_dataframe_column_names,
    get_non_numeric_data,
    get_numeric_data,
    select_non_numeric_columns,
    select_numeric_columns,
    str_data_memory_usage,
    validations,
)


class DataFrameParser(DataFrame):
    """
    DataFrameParser is a subclass of pandas DataFrame that provides
    additional functionality for automatically parsing various file
    types into pandas DataFrames.

    The class supports parsing from CSV, JSON, Parquet, Excel, and Pickle
    files.
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

    _metadata = ["_ignore", "verbose"]

    _READERS: dict[FileExtension, PdReader] = {
        FileExtension.CSV: read_csv,
        FileExtension.JSON: read_json,
        FileExtension.PARQUET: read_parquet,
        FileExtension.EXCEL: read_excel,
        FileExtension.PICKLE: read_pickle,
    }

    # ToDo add support for reading specific amount of columns and rows.
    def __init__(
        self,
        path_or_buf: FilePath | BytesIO | dict | np.ndarray | list,
        *,
        extension: FileExtension | str | None = None,
        ignore_wrong_properties: bool = False,
        verbose: bool = False,
        **properties,
    ) -> None:
        self.verbose = verbose
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

        if self.verbose:
            logging.debug("Starting data ingestion process...")

        if isinstance(path_or_buf, (np.ndarray, dict, list)):
            df = self._buf_loader(path_or_buf, **properties)

        elif isinstance(path_or_buf, (str, PathLike, BytesIO)):
            extension = FileExtension.parse(
                extension=extension, file=path_or_buf
            )
            path_or_buf = cast(FilePath, path_or_buf)
            df = self._file_loader(path_or_buf, extension, **properties)

        else:
            raise TypeError(
                "Unsupported type ({}) for path_or_buf. Supported "
                "types are (str, os.PathLike, BytesIO, dict, "
                "np.ndarray).".format(type(path_or_buf))
            )

        if self.verbose:
            logging.debug(
                "✅ Done! Data ingestion process completed. DataFrame is "
                "ready for use."
            )
            shape = df.shape
            # logging.debug(f"DataFrame columns: {shape[0]} | rows: {shape[1]}")
            tab: LiteralString = "\t" * 7
            logging.debug(
                "DataFrame Shape\t 🔻"
                f"\n{tab} _______\n{tab}"
                f"|columns| {shape[0]:>1}"
                f"\n{tab} _______\n{tab}"
                f"| rows  | {shape[1]:>1}"
            )

            mem = str_data_memory_usage(df, unit="KB", deep=True)
            logging.debug(f"DataFrame size in memory: {mem} ")
            logging.debug(f"DataFrame dtypes\n{df.dtypes} ")
            print(f"DataFrame head: {df.head(3)} ")

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
        uses the reader function to load the DataFrame from the file or
        stream.

        Parameters
        ----------
        path : FilePath
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
        # ToDo fix shouldn't be in for BytesIO, cast it later on.
        if not isinstance(path, BytesIO) and not file_exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")

        if self.verbose:
            logging.debug(f"Loading DataFrame from {path} ...")

        if extension:
            FileExtension.parse(extension=extension, file=path)
        reader = self._get_reader(extension)
        if not self._ignore:
            properties = self.__check_fix_properties(
                func=reader,
                **properties,
            )

        return reader(path, **properties)

    @staticmethod
    def __check_fix_properties(func: Callable[..., Any], **kwargs) -> dict:
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

    def get_column_names(self) -> list[str]:
        """
        Returns the column names of the DataFrame.

        Returns
        -------
        list[str]
            The column names of the DataFrame.
        """
        return get_dataframe_column_names(self)

    def get_column_types(self, parsed=False) -> dict[str, Any]:
        """
        Get the data types of the DataFrame's columns.

        This method returns a dictionary where the keys are the column names
        of the DataFrame and the values are the data types of these columns.
        If the `parsed` argument is `True`, the data types are parsed using
        the `_parse_types` method.

        Parameters
        ----------
        parsed : bool, optional
            Whether to parse the data types using the `_parse_types` method,
            by default False

        Returns
        -------
        dict[str, Any]
            A dictionary where the keys are the column names of the DataFrame
            and the values are the data types of these columns.
        """
        if not parsed:
            return self.dtypes.to_dict(into=dict)

        return self._parse_types()

    def get_numeric_columns(self) -> list[str] | None:
        """
        Returns the numeric columns of the DataFrame.

        Returns
        -------
        list[str] | None
            The numeric columns of the DataFrame.
        """
        return select_numeric_columns(self)

    def get_non_numeric_columns(self) -> list[str] | None:
        """
        Returns the non-numeric columns of the DataFrame.

        Returns
        -------
        list[str] | None
            The non-numeric columns of the DataFrame.
        """
        return select_non_numeric_columns(self)

    def get_non_numeric_data(self) -> DataFrame | None:
        """
        Returns the non-numeric data of the DataFrame.

        Returns
        -------
        DataFrame
            The non-numeric data of the DataFrame.
        """
        return get_non_numeric_data(self)

    def get_numeric_data(self) -> DataFrame | None:
        """
        Returns the numeric data of the DataFrame.

        Returns
        -------
        DataFrame
            The numeric data of the DataFrame.
        """
        return get_numeric_data(self)

    def _parse_types(self) -> dict[str, str]:
        """
        Parse the data types of the DataFrame's columns to their kind codes.

        This method applies a function to each data type of the DataFrame's
        columns that returns the kind code of the data type. The kind code
        is a character code representing the type of the data. For example,
        'b' represents boolean, 'i' represents signed integer.
        'u' represents unsigned integer, 'f' represents floating-point.
        'c' represents complex floating-point, 'O' represents object.
        'S' represents byte string.
        'U' represents Unicode string.
        'V' represents void.

        Returns
        -------
        dict[str, str]
            A dictionary where the keys are the column names of the DataFrame
            and the values are the kind codes of the data types of these
            columns.
        """
        parsed_types = {}
        for col in self.columns:
            parsed_types[col] = self[col].dtype.kind

        return parsed_types

    # @override
    def __new__(cls, *args, **kwargs) -> Self:
        """
        Creates a new instance of the DataFrameParser class.

        This method overrides the default constructor to add the
        `_ignore` attribute to the instance.

        Returns
        -------
        DataFrameParser
            The new instance of the DataFrameParser class.
        """
        return super(DataFrameParser, cls).__new__(cls)
