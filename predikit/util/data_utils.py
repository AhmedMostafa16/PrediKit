from pandas import DataFrame

from predikit._typing import MemoryUnit

# # tf currently not supported by python 3.12 | TODO: check for alternatives
# def split_dataset(
#     dataset: tf.Data.Dataset, validation_split: float = 0.25
# ) -> (tf.Data.Dataset, tf.Data.Dataset):
#     """Split dataset into training and validation sets.


#     Args:
#         dataset (tf.Data.Dataset): The entire dataset to be split.
#         validation_split (float): The split ratio for the validation set.

#     Returns:
#         A tuple of tf.Data.Dataset objects representing the training and
#         validation sets.
#     """
#     ...


def get_dataframe_column_names(dataframe: DataFrame) -> list[str]:
    """
    Get the column names of the DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        The DataFrame to retrieve its column names.

    Returns
    -------
    list[str]
        The column names of the DataFrame.
    """
    return dataframe.columns.tolist()


def select_numeric_columns(
    dataframe: DataFrame, columns: list[str] | None = None
) -> list[str] | None:
    """
    Select the numeric columns from the DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        The DataFrame to select the numeric columns from.
    columns : list[str] | None, optional
        The columns to consider, by default None

    Returns
    -------
    list[str] | None
        The numeric columns from the DataFrame, or None if there are no
        numeric columns.
    """
    if columns:
        dataframe = dataframe[columns]

    numeric_columns = dataframe.select_dtypes(include="number").columns

    return None if numeric_columns.empty else numeric_columns.tolist()


def select_non_numeric_columns(
    dataframe: DataFrame, columns: list[str] | None = None
) -> list[str] | None:
    """
    Select the non-numeric columns from the DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        The DataFrame to select the non-numeric columns from.
    columns : list[str] | None, optional
        The columns to consider, by default None

    Returns
    -------
    list[str] | None
        The non-numeric columns from the DataFrame, or None if there are no
        non-numeric columns.
    """
    if columns:
        dataframe = dataframe[columns]

    non_numeric_columns = dataframe.select_dtypes(exclude="number").columns
    return None if non_numeric_columns.empty else non_numeric_columns.tolist()


def get_non_numeric_data(
    dataframe: DataFrame, columns: list[str] | None = None
) -> DataFrame | None:
    """
    Get the non-numeric data from the DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        The DataFrame to get the non-numeric data from.
    columns : list[str] | None, optional
        The columns to consider, by default None

    Returns
    -------
    DataFrame | None
        The non-numeric data from the DataFrame, or None if there is no
        non-numeric data.
    """
    non_numeric_columns = select_non_numeric_columns(dataframe, columns)
    return None if not non_numeric_columns else dataframe[non_numeric_columns]


def get_numeric_data(
    dataframe: DataFrame, columns: list[str] | None = None
) -> DataFrame | None:
    """
    Get the numeric data from the DataFrame.

    Parameters
    ----------
    dataframe : DataFrame
        The DataFrame to get the numeric data from.
    columns : list[str] | None, optional
        The columns to consider, by default None

    Returns
    -------
    DataFrame | None
        The numeric data from the DataFrame, or None if there is no
        numeric data.
    """
    numeric_columns = select_numeric_columns(dataframe, columns)
    return None if not numeric_columns else dataframe[numeric_columns]


def exclude_from_columns(
    columns: list[str], exclude: list[str] | None
) -> list[str]:
    """
    Exclude the columns from the list of columns.

    Parameters
    ----------
    columns : list[str]
        The list of columns to exclude from.
    exclude : list[str]
        The list of columns to exclude.

    Returns
    -------
    list[str]
        The list of columns excluding the excluded columns.
    """
    return (
        columns
        if not exclude
        else [column for column in columns if column not in exclude]
    )


def convert_memory_size(size: int, unit: MemoryUnit) -> float:
    """
    Convert a memory size from bytes to the specified unit.

    This function takes a memory size in bytes and a unit of memory, and
    returns the memory size converted to the specified unit. The units can be
    bytes (B), kilobytes (KB), megabytes (MB), or gigabytes (GB).

    If an invalid unit is provided, a ValueError is raised.

    Parameters
    ----------
    size : int
        The memory size in bytes.
    unit : {'B', 'KB', 'MB', 'GB'}
        The unit to which the memory size should be converted.

    Returns
    -------
    float
        The memory size converted to the specified unit.

    Raises
    ------
    ValueError
        If the specified unit is not one of 'B', 'KB', 'MB', or 'GB'.
ode
    Examples
    --------
    >>> print(convert_memory_size(1024, 'KB'))
    1.0
    """
    conversion_factors = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    try:
        return size / conversion_factors[unit]
    except KeyError:
        valid_units = ", ".join(conversion_factors.keys())
        raise ValueError(
            f"Invalid unit: {unit}. Valid units are {valid_units}."
        )

def data_memory_usage(
    df: DataFrame, unit: MemoryUnit = "MB", deep: bool = False
) -> float:
    """
    Calculate and return the memory usage of a DataFrame in a specified unit.

    This function calculates the total memory usage of a DataFrame, including
    all columns and indices, and returns it in the specified unit. The units
    can be bytes (B), kilobytes (KB), megabytes (MB), or gigabytes (GB).

    If `deep` is True, the memory usage of data buffers for objects is
    inspected deeply and may be more accurate.

    Parameters
    ----------
    df : DataFrame
        The DataFrame whose memory usage is to be calculated.
    unit : {'B', 'KB', 'MB', 'GB'}, optional
        The unit in which to return the memory usage. By default, it is 'MB'.
    deep : bool, optional
        If True, introspect data buffers of object columns, which can be more
        accurate. By default, it is False.

    Returns
    -------
    float
        The memory usage of the DataFrame in the specified unit.

    Examples
    --------
    >>> df = pd.DataFrame({'A': range(1, 1000000)})
    >>> # Here, df is a DataFrame with 1 million rows and one column 'A'.
    >>> print(data_memory_usage(df, 'MB'))
    7.63
    """
    memory_usage = df.memory_usage(deep=deep).sum()
    return convert_memory_size(memory_usage, unit)


def str_data_memory_usage(
    df: DataFrame,
    unit: MemoryUnit = "MB",
    precision: int = 2,
    deep: bool = False,
) -> str:
    """
    Calculate and return the memory usage of a DataFrame in a specified unit
    as a string.

    This function extends the `data_memory_usage` function by returning the
    memory usage as a string with the unit of memory appended to the end.

    If `deep` is True, the memory usage of data buffers for objects is
    inspected deeply and may be more accurate.

    Parameters
    ----------
    df : DataFrame
        The DataFrame whose memory usage is to be calculated.
    unit : {'B', 'KB', 'MB', 'GB'}, optional
        The unit in which to return the memory usage. By default, it is 'MB'.
    deep : bool, optional
        If True, introspect data buffers of object columns, which can be more
        accurate. By default, it is False.
    precision : int, optional
        The number of decimal places to round to, by default 2.

    Returns
    -------
    str
        The memory usage of the DataFrame in the specified unit as a string.

    Examples
    --------
    >>> df = pd.DataFrame({'A': range(1, 1000000)})
    >>> # Here, df is a DataFrame with 1 million rows and one column 'A'.
    >>> print(str_data_memory_usage(df, 'MB'))
    '7.63 MB'
    """
    memory_usage = data_memory_usage(df, unit, deep)
    return f"{memory_usage:.{precision}f} {unit.upper()}"
