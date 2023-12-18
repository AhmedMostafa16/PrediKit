from os import PathLike
from typing import Callable, TypeAlias

from pandas import DataFrame

Number: TypeAlias = int | float

PdReader: TypeAlias = Callable[..., DataFrame]
FilePath: TypeAlias = str | PathLike[str]
DfExporter: TypeAlias = Callable[..., str | None]