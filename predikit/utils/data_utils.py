from pandas import DataFrame

# # tf currently not supported by python 3.12 | TODO: check for alternatives
# def split_dataset(
#     dataset: tf.Data.Dataset, validation_split: float = 0.25
# ) -> (tf.Data.Dataset, tf.Data.Dataset):
#     """Split dataset into training and validation sets.


#     Args:
#         dataset (tf.Data.Dataset): The entire dataset to be split.
#         validation_split (float): The split ratio for the validation set.

#     Returns:
#         A tuple of tf.Data.Dataset objects representing the training and validation sets.
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
    return list(dataframe.columns)


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
        The numeric columns from the DataFrame, or None if there are no numeric columns.
    """
    if columns:
        dataframe = dataframe[columns]

    numeric_columns = dataframe.select_dtypes(include="number").columns

    return None if numeric_columns.empty else list(numeric_columns)


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
        The non-numeric columns from the DataFrame, or None if there are no non-numeric columns.
    """
    if columns:
        dataframe = dataframe[columns]

    non_numeric_columns = dataframe.select_dtypes(exclude="number").columns
    return None if non_numeric_columns.empty else list(non_numeric_columns)


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
        The non-numeric data from the DataFrame, or None if there is no non-numeric data.
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
        The numeric data from the DataFrame, or None if there is no numeric data.
    """
    numeric_columns = select_numeric_columns(dataframe, columns)
    return None if not numeric_columns else dataframe[numeric_columns]
