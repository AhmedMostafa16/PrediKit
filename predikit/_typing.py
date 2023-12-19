from os import PathLike
from typing import (
    Callable,
    Literal,
)

from pandas import DataFrame

type Number = int | float

type PdReader = Callable[..., DataFrame]
type FilePath = str | PathLike[str]
type DfExporter = Callable[..., str | None]
type MemoryUnit = Literal["B", "KB", "MB", "GB"]
