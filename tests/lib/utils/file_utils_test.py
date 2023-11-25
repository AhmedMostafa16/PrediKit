import pandas as pd
import pytest

from lib.utils.file_utils import Extension, FileUtils


@pytest.mark.parametrize(
    "extension,criteria,expected",
    [
        ("csv", ["csv", "json"], True),
        ("csv", ["json", "pkl"], False),
        ("xlsx", ["xlsx", "xls"], True),
        ("xlsx", ["xls"], False),
    ],
)
def test_is_type_of(extension, criteria, expected):
    assert FileUtils.is_type_of(extension, criteria) == expected


def test_get_properties():
    properties = FileUtils.get_properties(pd.read_csv)
    assert "filepath_or_buffer" in properties
    assert "sep" in properties
    assert "delimiter" in properties


@pytest.mark.parametrize(
    "artificial_file, expected_reader_type",
    [
        ("foo.json", FileUtils.READERS[Extension.JSON]),
        ("bar.xls", FileUtils.READERS[Extension.EXCEL]),
        ("baz.xlsx", FileUtils.READERS[Extension.EXCEL]),
        ("qux.pkl", FileUtils.READERS[Extension.PICKLE]),
        ("thud.csv", FileUtils.READERS[Extension.CSV]),
        ("corge.p", FileUtils.READERS[Extension.PICKLE]),
        ("xyzyy.pickle", FileUtils.READERS[Extension.PICKLE]),
    ],
)
def test_read_type_artificial_data(artificial_file, expected_reader_type):
    assert (
        FileUtils.get_reader(FileUtils.get_extension(artificial_file))
        == expected_reader_type
    )


def test_extension_from_string():
    assert Extension.from_string("csv") == Extension.CSV
    assert Extension.from_string("xlsx") == Extension.EXCEL
    assert Extension.from_string("json") == Extension.JSON
    assert Extension.from_string("pkl") == Extension.PICKLE
    with pytest.raises(ValueError):
        Extension.from_string("unsupported_extension")


def test_get_extension():
    assert FileUtils.get_extension("test.csv") == Extension.CSV
    assert FileUtils.get_extension("test.xlsx") == Extension.EXCEL
    assert FileUtils.get_extension("test.json") == Extension.JSON
    assert FileUtils.get_extension("test.pkl") == Extension.PICKLE


def test_get_reader_call():
    assert callable(FileUtils.get_reader(Extension.CSV))
    assert callable(FileUtils.get_reader(Extension.EXCEL))
    assert callable(FileUtils.get_reader(Extension.JSON))
    assert callable(FileUtils.get_reader(Extension.PICKLE))


@pytest.mark.parametrize(
    "extension, expected",
    [
        (Extension.CSV, pd.read_csv),
        (Extension.JSON, pd.read_json),
        (Extension.PICKLE, pd.read_pickle),
        (Extension.EXCEL, pd.read_excel),
    ],
)
def test_get_reader(extension, expected):
    assert FileUtils.get_reader(extension) == expected
