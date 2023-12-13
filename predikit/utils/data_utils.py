# tf currently not supported by python 3.12
# TODO: check for alternatives
from pandas import DataFrame

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


def numeric_columns_selector(
    data: DataFrame, columns: list[str] | None = None
) -> list[str] | None:
    numeric_columns = []

    if columns is None:
        columns = data.columns.tolist()

    for col in columns:
        if data[col].dtype.kind not in "iuf":
            continue
        numeric_columns.append(col)

    return None if not numeric_columns else numeric_columns


def non_numeric_selector(
    data: DataFrame, columns: list[str] | None = None
) -> DataFrame | None:
    non_numeric_columns = []

    if columns is None:
        columns = data.columns.tolist()

    for col in data.columns:
        if data[col].dtype.kind not in "O":
            continue
        non_numeric_columns.append(col)

    return None if not non_numeric_columns else data[non_numeric_columns]
