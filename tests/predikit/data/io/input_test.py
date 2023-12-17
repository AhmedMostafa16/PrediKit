from unittest.mock import (
    mock_open,
    patch,
)

import pandas as pd
import pytest

from predikit import (
    DataFrameParser,
    FileExtension,
)

# Mock data for testing
mock_data = "a,b,c\n1,2,3\n4,5,6\n"


@pytest.fixture
def mock_file():
    return mock_open(read_data=mock_data)


def test_init():
    parser = DataFrameParser("file.csv")
    assert parser._file == "file.csv"
    assert parser._extension == FileExtension.CSV
    assert parser._properties == {}


def test_init_with_properties():
    parser = DataFrameParser("file.csv", header=0, sep=",")
    assert parser._file == "file.csv"
    assert parser._extension == FileExtension.CSV
    assert parser._properties == {"header": 0, "sep": ","}


def test_get_reader():
    parser = DataFrameParser("file.csv")
    assert parser._get_reader() == pd.read_csv


def test_get_properties():
    parser = DataFrameParser("file.csv")
    properties = parser.get_properties()
    assert "filepath_or_buffer" in properties
    assert "sep" in properties


@patch("pandas.read_csv")
def test_load(mock_read_csv, mock_file):
    mock_read_csv.return_value = pd.DataFrame()
    with patch("builtins.open", new=mock_file):
        parser = DataFrameParser("file.csv")
        df = parser.parse()
        assert isinstance(df, pd.DataFrame)


@patch("pandas.read_csv")
def test_load_with_invalid_properties(mock_read_csv, mock_file):
    mock_read_csv.return_value = pd.DataFrame()
    with patch("builtins.open", new=mock_file):
        parser = DataFrameParser(
            "file.csv", invalid_param=10
        )  # header is out of range
        df = parser.parse()
        assert isinstance(df, pd.DataFrame)
