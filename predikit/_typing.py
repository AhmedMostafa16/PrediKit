from os import PathLike
from typing import Callable

from pandas import DataFrame

from predikit.data.preprocessors.data_cleansing import (
    MissingValuesProcessor,
    OutliersProcessor,
)
from predikit.data.preprocessors.encoders import (
    BinaryEncoder,
    CategoricalEncoder,
)

type Number = int | float

type PdReader = Callable[..., DataFrame]
type FilePath = str | PathLike[str]


type OutliersEncoder = OutliersProcessor | None
type MissingValuesEncoder = MissingValuesProcessor | None
type CatEncoder = CategoricalEncoder | None
type BinEncoder = BinaryEncoder | None
