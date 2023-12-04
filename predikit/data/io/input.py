from io import BytesIO

from result import Err
from result import Ok
from result import Result

from ...utils import Extension
from ...utils.io_utils import get_reader
from ...utils.validations import Validations


def load_file_as_df(file: BytesIO, ext: Extension, **props) -> Result:
    """
    Load a file as a pandas DataFrame.

    Parameters
    ----------
    file : BytesIO
        The file object to load.
    ext : Extension
        The file extension indicating the file format.
    **props : dict
        Additional properties to pass to the file reader.

    Returns
    -------
    ResDfOrNone
        A Result object containing either a pandas DataFrame or an error message.

    Notes
    -----
    This function uses the `get_reader` function to obtain the appropriate file reader based on the file extension.
    It then validates the additional properties using the `Validations.validate_reader_kwargs` function.
    Finally, it reads the file using the obtained reader and the provided properties, and returns the result as a pandas DataFrame.

    If any error occurs during the loading process, an error message is returned instead of the DataFrame.

    Examples
    --------
    >>> file = BytesIO(b"col1,col2\\n1,2\\n3,4")
    >>> ext = Extension.CSV
    >>> result = load_file_as_df(file, ext)
    >>> result.is_ok()
    True
    >>> result.unwrap()
        col1  col2
    0     1     2
    1     3     4
    """

    try:
        reader = get_reader(ext)

        valid_prop = Validations.validate_reader_kwargs(reader, props)
        props = {} if not valid_prop else props

        df = reader(file, **props)
        return Ok(df)
    except Exception as e:
        return Err(f"error loading file as DataFrame: {e}")
