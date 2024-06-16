from os import PathLike
from typing import (
    Any,  # noqa: F401
    Callable,
    Literal,
    TypeAlias,
    Union,
)

import numpy as np
import numpy.typing
import pandas as pd
from pandas import DataFrame
from scipy import sparse

Number: TypeAlias = int | float
ArrayLike: TypeAlias = numpy.typing.ArrayLike
MatrixLike: TypeAlias = np.ndarray | pd.DataFrame | pd.Series

SEQUENCE = (list, tuple, np.ndarray, pd.Series)
SEQUENCE_LIKE: TypeAlias = Union[list, tuple, np.ndarray, pd.Series]
DATAFRAME_LIKE: TypeAlias = Union[
    dict, list, tuple, np.ndarray, sparse.spmatrix, pd.DataFrame
]
TARGET_LIKE: TypeAlias = Union[int, str, list, tuple, np.ndarray, pd.Series]

PdReader: TypeAlias = Callable[..., DataFrame]
FilePath: TypeAlias = str | PathLike[str]
DfExporter: TypeAlias = Callable[..., str | None]
MemoryUnit: TypeAlias = Literal["B", "KB", "MB", "GB"]
