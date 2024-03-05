from os import PathLike
from typing import (
    Callable,
    Literal,
    TypeAlias,
)

from pandas import DataFrame, Series

Number: TypeAlias = int | float

PdReader: TypeAlias = Callable[..., DataFrame]
FilePath: TypeAlias = str | PathLike[str]
DfExporter: TypeAlias = Callable[..., str | None]
MemoryUnit: TypeAlias = Literal["B", "KB", "MB", "GB"]
