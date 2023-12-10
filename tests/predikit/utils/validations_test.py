from unittest.mock import MagicMock

import pandas as pd
import pytest

from predikit import validations as v


def test_validate_reader_kwargs_success():
    result = v.validate_reader_kwargs(
        pd.read_csv, {"filepath_or_buffer": "test.csv", "sep": ","}
    )

    assert result is True


def test_validate_reader_kwargs_invalid_key():
    result = v.validate_reader_kwargs(
        pd.read_csv, {"invalid_key": "test.csv", "sep": ","}
    )

    assert result is False


@pytest.mark.skip(reason="to be implemented")
def test_validate_reader_kwargs_invalid_type():
    result = v.validate_reader_kwargs(
        pd.read_csv, {"filepath_or_buffer": Exception, "sep": ","}
    )

    assert result is False


def test_validate_reader_kwargs_no_annotations():
    mock_reader = MagicMock()
    mock_reader.__annotations__ = {}

    result = v.validate_reader_kwargs(
        pd.read_csv, {"filepath_or_buffer": "test.csv", "sep": ","}
    )

    assert result is True
