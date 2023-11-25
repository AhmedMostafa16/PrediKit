import csv
from io import BytesIO
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def sample_datasets() -> list[str]:
    datasets = [
        "../../data/demo/airline_bumping.csv",
        "../../data/demo/movies.p",
        "../../data/demo/temperatures.csv",
        "../../data/demo/stations.p",
    ]
    return datasets


@pytest.fixture
def mock_csv_to_byte_io():
    dataset = "\n".join(
        [
            ",".join(["column1", "column2", "colum3"]),
            ",".join(["data1", "data2", "data3"]),
        ]
    )
    bytes_io = BytesIO(dataset.encode())

    mock_bytes_io = MagicMock(spec=BytesIO, return_value=bytes_io)
    return mock_bytes_io
