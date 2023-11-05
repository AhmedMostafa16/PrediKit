from io import BytesIO
from typing import TypeAlias

import pandas as pd

from lib.utils.file_utils import FileUtils
from lib.utils.result import Result
from lib.utils.validations import Validations

ResDfOrNone: TypeAlias = Result[pd.DataFrame] | Result[None]
Extension: TypeAlias = FileUtils.Extension


def load_file_as_df(file: BytesIO, ext: Extension, **props) -> ResDfOrNone:
    """
    Load a file as a pandas DataFrame.

    Args:
        file (BytesIO): The file to load.
        ext (FileUtils.Extension): The file extension.
        props: Properties of the Input Data Node.

    Returns:
        Result: A Result object containing either the loaded DataFrame or an error message.
    """
    try:
        reader = FileUtils.get_reader(ext)

        valid_prop = Validations.validate_reader_kwargs(reader, props)
        props = {} if not valid_prop else props

        df = reader(file, **props)
        return Result[pd.DataFrame](df)

    except Exception as e:
        return Result[None](error=str(e))


# Relative package imports are used here
# To run this you need to be at the root of the project
# then type python3 -m lib.data_processing.io.input
def main():
    sample = "./data/sample/temperatures.csv"
    with open(sample, "rb") as f:
        data = f.read()

    data_io = BytesIO(data)

    res = load_file_as_df(data_io, Extension.CSV)

    if not res.success:
        print(res.error)
        return

    if res.value is not None:
        print(res.value.head(3))


if __name__ == "__main__":
    main()
