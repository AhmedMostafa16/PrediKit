from io import BytesIO
from unittest.mock import patch

import pytest

from predikit.utils.io_utils import FileExtension


def test_from_string():
    assert FileExtension.from_string("csv") == FileExtension.CSV
    assert FileExtension.from_string("xlsx") == FileExtension.EXCEL
    with pytest.raises(ValueError):
        FileExtension.from_string("unsupported_extension")

    # Test case insensitivity
    assert FileExtension.from_string("CSV") == FileExtension.CSV


def test_from_file():
    with patch("os.path.splitext") as mock_splitext:
        mock_splitext.return_value = ("/path/to/file", ".csv")
        assert FileExtension.from_file("/path/to/file.csv") == FileExtension.CSV

    # Test with different file path
    mock_splitext.return_value = ("/another/path/to/file", ".xlsx")
    assert (
        FileExtension.from_file("/another/path/to/file.xlsx")
        == FileExtension.EXCEL
    )


def test_parse():
    assert (
        FileExtension.parse(extension="csv", file="/path/to/file.csv")
        == FileExtension.CSV
    )
    assert (
        FileExtension.parse(
            extension=FileExtension.CSV, file="/path/to/file.csv"
        )
        == FileExtension.CSV
    )
    with patch("os.path.splitext") as mock_splitext:
        mock_splitext.return_value = ("/path/to/file", ".csv")
        assert (
            FileExtension.parse(file="/path/to/file.csv") == FileExtension.CSV
        )

    # Test with different file path
    mock_splitext.return_value = ("/another/path/to/file", ".xlsx")
    assert (
        FileExtension.parse(file="/another/path/to/file.xlsx")
        == FileExtension.EXCEL
    )

    with pytest.raises(NotImplementedError):
        FileExtension.parse(file=BytesIO(b"some data"))

    # Test with None extension and file
    with pytest.raises(ValueError):
        FileExtension.parse(extension=None, file=None)  # type: ignore
