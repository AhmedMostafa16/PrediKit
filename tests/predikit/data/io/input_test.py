from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from predikit.data.io.input import DataFrameParser
from predikit.utils import FileExtension

# Mock data for testing
mock_data = "a,b,c\n1,2,3\n4,5,6\n"


@pytest.fixture
def mock_file():
    return mock_open(read_data=mock_data)


def test_init():
    parser = DataFrameParser("file.csv")
    assert parser.file == "file.csv"
    assert parser.extension == FileExtension.CSV
    assert parser.properties == {}


def test_init_with_properties():
    parser = DataFrameParser("file.csv", header=0, sep=",")
    assert parser.file == "file.csv"
    assert parser.extension == FileExtension.CSV
    assert parser.properties == {"header": 0, "sep": ","}


def test_get_reader():
    parser = DataFrameParser("file.csv")
    assert parser.get_reader() == pd.read_csv


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
        df = parser.load()
        assert isinstance(df, pd.DataFrame)


@patch("pandas.read_csv")
def test_load_with_invalid_properties(mock_read_csv, mock_file):
    mock_read_csv.return_value = pd.DataFrame()
    with patch("builtins.open", new=mock_file):
        parser = DataFrameParser(
            "file.csv", invalid_param=10
        )  # header is out of range
        df = parser.load()
        assert isinstance(df, pd.DataFrame)
