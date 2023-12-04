# tf currently not supported by python 3.12
# TODO: check for alternatives


def split_dataset(
    dataset: tf.Data.Dataset, validation_split: float = 0.25
) -> (tf.Data.Dataset, tf.Data.Dataset):
    """Split dataset into training and validation sets.


    Args:
        dataset (tf.Data.Dataset): The entire dataset to be split.
        validation_split (float): The split ratio for the validation set.

    Returns:
        A tuple of tf.Data.Dataset objects representing the training and validation sets.
    """
    ...
