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
        df.dtypes.tolist(),
        list(df.shape),
    )


# def get_column_names_from_node_input(node_input: BaseInput):
#     """
#     Get the column names from a node input.
#     """
#     if node_input.input_type == "dataset":
#         return node_input.enforce(node_input).columns.tolist()
#     return []
