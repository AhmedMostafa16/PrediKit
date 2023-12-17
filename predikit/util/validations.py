import inspect

from predikit._typing import PdReader

"""
A utility class for validating data and inputs.
"""


def validate_reader_kwargs(reader: PdReader, kwargs) -> bool:
    """
    Validates the keyword arguments passed to a Pandas reader function.

    Args:
        cls (type): The class that the reader function belongs to.
        reader (PdRead): The Pandas reader function to validate the keyword
        arguments for.
        kwargs (dict): The keyword arguments to validate.

    Returns:
        bool: True if all keyword arguments are valid, False otherwise.
    """
    reader_params = inspect.signature(reader).parameters
    for k, v in kwargs.items():
        # kwargs key against parameter name
        if k not in reader_params:
            return False

        expected_type = reader_params[k].annotation

        # kwargs value against parameter data type
        if expected_type is inspect.Parameter.empty:
            continue

    return True
