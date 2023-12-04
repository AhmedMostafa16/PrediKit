# """
# This module contains unit tests for the input module of the data_processing package,
# responsible for the Input Data Node.
# """

# from io import BytesIO
# from unittest.mock import MagicMock, patch

# import pandas as pd
# import pytest

# from predikit.data.io.input import load_file_as_df
# from predikit.utils import Extension
# from predikit.utils.io_utils import get_reader
# from predikit.utils.validations import Validations


# @pytest.fixture
# def csv_data():
#     return b"column1,column2\nvalue1,value2"


# @pytest.fixture
# def csv_file(csv_data):
#     return BytesIO(csv_data)


# @pytest.fixture
# def mock_reader():
#     mock = MagicMock()
#     mock.return_value = pd.DataFrame(
#         {"column1": ["value1"], "column2": ["value2"]}
#     )
#     return mock


# @pytest.fixture
# def mock_validate_reader_kwargs():
#     mock = MagicMock()
#     mock.return_value = True
#     return mock


# @patch("predikit.utils.io_utils.get_reader")
# @patch.object(Validations, "validate_reader_kwargs")
# def test_load_file_as_df_success(
#     mock_validate_reader_kwargs, mock_reader, csv_file
# ):
#     mock_reader.return_value = mock_reader
#     mock_validate_reader_kwargs.return_value = mock_validate_reader_kwargs

#     result = load_file_as_df(csv_file, Extension.CSV)

#     mock_reader.assert_any_call(Extension.CSV)
#     mock_validate_reader_kwargs.assert_called_once_with(mock_reader, {})

#     assert result.value is not None
#     assert result.success
#     assert result.value.equals(
#         pd.DataFrame({"column1": ["value1"], "column2": ["value2"]})
#     )
#     assert result.error is None


# @patch("predikit.utils.io_utils.get_reader")
# @patch.object(Validations, "validate_reader_kwargs")
# def test_load_file_as_df_invalid_props(
#     mock_validate_reader_kwargs, mock_reader, csv_file
# ):
#     mock_reader.return_value = mock_reader
#     mock_validate_reader_kwargs.return_value = False

#     result = load_file_as_df(csv_file, Extension.CSV, invalid_prop="invalid")

#     mock_reader.assert_any_call(Extension.CSV)
#     mock_validate_reader_kwargs.assert_called_once_with(
#         mock_reader, {"invalid_prop": "invalid"}
#     )

#     assert result.error is None
#     assert result.value is not None
#     assert result.success
#     assert result.value.equals(
#         pd.DataFrame({"column1": ["value1"], "column2": ["value2"]})
#     )


# @patch("predikit.utils.io_utils.get_reader")
# def test_load_file_as_df_exception(mock_reader, csv_file):
#     mock_reader.side_effect = Exception("Test exception")

#     result = load_file_as_df(csv_file, Extension.CSV)

#     mock_reader.assert_called_once_with(Extension.CSV)

#     assert result.value is None
#     assert result.error == "Test exception"
#     assert not result.success


# @patch("predikit.utils.io_utils.get_reader")
# @patch.object(Validations, "validate_reader_kwargs")
# def test_load_file_as_df_with_kwargs(
#     mock_validate_reader_kwargs, mock_reader, csv_file
# ):
#     mock_reader.return_value = mock_reader
#     mock_validate_reader_kwargs.return_value = True

#     result = load_file_as_df(csv_file, Extension.CSV, sep=",", header=0)

#     mock_reader.assert_any_call(Extension.CSV)
#     mock_validate_reader_kwargs.assert_called_once_with(
#         mock_reader, {"sep": ",", "header": 0}
#     )

#     assert result.value is not None
#     assert result.success
#     assert result.value.equals(
#         pd.DataFrame({"column1": ["value1"], "column2": ["value2"]})
#     )
#     assert result.error is None


# @patch("predikit.utils.io_utils.get_reader")
# def test_load_file_as_df_no_reader(mock_reader, csv_file):
#     mock_reader.return_value = None

#     result = load_file_as_df(csv_file, Extension.CSV)

#     mock_reader.assert_called_once_with(Extension.CSV)

#     assert result.value is None
#     assert not result.success
#     assert result.error == "None is not a callable object"
