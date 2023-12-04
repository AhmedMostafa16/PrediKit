from ._base import BinaryEncodingStrategies
from ._base import CategoricalEncodingStrategies
from ._base import MissingValueStrategy
from ._base import OutlierDetectionMethod
from ._base import Preprocessor
from .data_cleansing import MissingValuesProcessor
from .data_cleansing import OutliersProcessor
from .encoders import BinaryEncoder
from .encoders import CategoricalEncoder

type OutliersEncoder = OutliersProcessor | None
type MissingValuesEncoder = MissingValuesProcessor | None
type CatEncoder = CategoricalEncoder | None
type BinEncoder = BinaryEncoder | None


class DataPrep(Preprocessor):
    _clean_missing_enc: MissingValuesEncoder = None
    _clean_outliers_enc: OutliersEncoder = None
    _binary_encoder: BinEncoder = None
    _cat_encoder: CatEncoder = None

    def __init__(
        self,
        clean_missing: bool = True,
        clean_strategy: MissingValueStrategy = MissingValueStrategy.MEAN,
        clean_outliers: bool = True,
        outliers_method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        outliers_threshold: float = 1.5,
        cat_encoders_strategies: list[CategoricalEncodingStrategies] = [
            CategoricalEncodingStrategies.HelmertEncoder,
            CategoricalEncodingStrategies.CountEncoder,
        ],
        binary_encoders_strategies: list[BinaryEncodingStrategies] = [
            BinaryEncodingStrategies.OrdinalEncoder,
        ],
        drop_invariant: bool = False,
        normalization: bool = False,
        random_state: int = 42,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        self.cat_encoders_strategies = cat_encoders_strategies
        self.binary_encoders_strategies = binary_encoders_strategies
        self.random_state = random_state

        self._clean_missing = clean_missing
        self._clean_strategy = clean_strategy
        self._clean_outliers = clean_outliers
        self._outliers_method = outliers_method
        self._outliers_threshold = outliers_threshold
        self._drop_invariant = drop_invariant
        self._normalization = normalization
