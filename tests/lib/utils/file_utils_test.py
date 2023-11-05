import pandas as pd
import pytest

from lib.utils.file_utils import FileUtils

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
        ("foo.json", FileUtils.READERS[FileUtils.Extension.JSON]),
        ("bar.xls", FileUtils.READERS[FileUtils.Extension.EXCEL]),
        ("baz.xlsx", FileUtils.READERS[FileUtils.Extension.EXCEL]),
        ("qux.pkl", FileUtils.READERS[FileUtils.Extension.PICKLE]),
        ("thud.csv", FileUtils.READERS[FileUtils.Extension.CSV]),
        ("corge.p", FileUtils.READERS[FileUtils.Extension.PICKLE]),
        ("xyzyy.pickle", FileUtils.READERS[FileUtils.Extension.PICKLE]),
    ],
)
def test_read_type_artificial_data(artificial_file, expected_reader_type):
    assert (
        FileUtils.get_reader(FileUtils.get_extension(artificial_file))
        == expected_reader_type
    )


def test_extension_from_string():
    assert FileUtils.Extension.from_string("csv") == FileUtils.Extension.CSV
    assert FileUtils.Extension.from_string("xlsx") == FileUtils.Extension.EXCEL
    assert FileUtils.Extension.from_string("json") == FileUtils.Extension.JSON
    assert FileUtils.Extension.from_string("pkl") == FileUtils.Extension.PICKLE
    with pytest.raises(ValueError):
        FileUtils.Extension.from_string("unsupported_extension")


def test_get_extension():
    assert FileUtils.get_extension("test.csv") == FileUtils.Extension.CSV
    assert FileUtils.get_extension("test.xlsx") == FileUtils.Extension.EXCEL
    assert FileUtils.get_extension("test.json") == FileUtils.Extension.JSON
    assert FileUtils.get_extension("test.pkl") == FileUtils.Extension.PICKLE


def test_get_reader_call():
    assert callable(FileUtils.get_reader(FileUtils.Extension.CSV))
    assert callable(FileUtils.get_reader(FileUtils.Extension.EXCEL))
    assert callable(FileUtils.get_reader(FileUtils.Extension.JSON))
    assert callable(FileUtils.get_reader(FileUtils.Extension.PICKLE))


@pytest.mark.parametrize(
    "extension, expected",
    [
        (FileUtils.Extension.CSV, pd.read_csv),
        (FileUtils.Extension.JSON, pd.read_json),
        (FileUtils.Extension.PICKLE, pd.read_pickle),
        (FileUtils.Extension.EXCEL, pd.read_excel),
    ],
)
def test_get_reader(extension, expected):
    assert FileUtils.get_reader(extension) == expected
