import pandas


def get_available_dataset_formats():
    available_formats = [
        ".csv",
        ".json",
        ".parquet",
        ".pickle",
        ".feather",
        ".xls",
        ".xlsx",
    ]
    return sorted(list(available_formats))


def get_dataframe_fields(df: pandas.DataFrame):
    """
    Get information about the fields in a DataFrame.
    """
    return (
        df.columns.tolist(),
        df.to_dict(orient="split"),
        df.index.tolist(),
        str(df.dtypes),
        df.shape,
    )
