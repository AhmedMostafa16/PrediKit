from os import PathLike
from typing import Callable

from pandas import DataFrame

type Number = int | float

type PdReader = Callable[..., DataFrame]
type FilePath = str | PathLike[str]
type DfExporter = Callable[..., str | None]
