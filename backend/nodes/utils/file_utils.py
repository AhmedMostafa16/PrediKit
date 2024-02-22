def get_available_dataset_formats() -> list[str]:
    """
    Returns a sorted list of available dataset formats.
    """
    available_formats = [
        ".csv",
        ".feather",
        ".hdf5",
        ".json",
        ".parquet",
        ".xls",
        ".xlsx",
    ]
    return sorted(available_formats)
