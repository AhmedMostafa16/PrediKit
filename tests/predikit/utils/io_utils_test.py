import pandas as pd
import pytest

import predikit.utils.io_utils as iu
from predikit.utils import Extension


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
    assert iu.is_type_of(extension, criteria) == expected


def test_get_properties():
    properties = iu.get_properties(pd.read_csv)
    assert "filepath_or_buffer" in properties
    assert "sep" in properties
    assert "delimiter" in properties


@pytest.mark.parametrize(
    "artificial_file, expected_reader_type",
    [
        ("foo.json", iu.READERS[Extension.JSON]),
        ("bar.xls", iu.READERS[Extension.EXCEL]),
        ("baz.xlsx", iu.READERS[Extension.EXCEL]),
        ("qux.pkl", iu.READERS[Extension.PICKLE]),
        ("thud.csv", iu.READERS[Extension.CSV]),
        ("corge.p", iu.READERS[Extension.PICKLE]),
        ("xyzyy.pickle", iu.READERS[Extension.PICKLE]),
    ],
)
def test_read_type_artificial_data(artificial_file, expected_reader_type):
    assert (
        iu.get_reader(iu.get_extension(artificial_file)) == expected_reader_type
    )


def test_extension_from_string():
    assert Extension.from_string("csv") == Extension.CSV
    assert Extension.from_string("xlsx") == Extension.EXCEL
    assert Extension.from_string("json") == Extension.JSON
    assert Extension.from_string("pkl") == Extension.PICKLE
    with pytest.raises(ValueError):
        Extension.from_string("unsupported_extension")


def test_get_extension():
    assert iu.get_extension("test.csv") == Extension.CSV
    assert iu.get_extension("test.xlsx") == Extension.EXCEL
    assert iu.get_extension("test.json") == Extension.JSON
    assert iu.get_extension("test.pkl") == Extension.PICKLE


def test_get_reader_call():
    assert callable(iu.get_reader(Extension.CSV))
    assert callable(iu.get_reader(Extension.EXCEL))
    assert callable(iu.get_reader(Extension.JSON))
    assert callable(iu.get_reader(Extension.PICKLE))


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
    assert iu.get_reader(extension) == expected
