from os import PathLike
import numpy as np
import numpy.typing
import pandas as pd
from typing import (
    Callable,
    Literal,
    TypeAlias,
    Any,
)

from pandas import DataFrame

Number: TypeAlias = int | float
ArrayLike: TypeAlias = numpy.typing.ArrayLike
MatrixLike: TypeAlias = np.ndarray | pd.DataFrame

PdReader: TypeAlias = Callable[..., DataFrame]
FilePath: TypeAlias = str | PathLike[str]
DfExporter: TypeAlias = Callable[..., str | None]
MemoryUnit: TypeAlias = Literal["B", "KB", "MB", "GB"]
