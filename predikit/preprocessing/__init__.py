"""
The :mod:`predikit.preprocessing` module includes data cleansing,
filtering and feature engineering methods.
"""

# ToDo: replace feature engineering with scaling, centering, normalization
# , methods.

__all__ = [
    "MissingValueStrategy",
    "OutlierDetectionMethod",
    "FeatureSelection",
    "NumericalInteractionFeatures",
    "DataPreparer",
    "MissingValuesProcessor",
    "OutliersProcessor",
    "EncodingStrategies",
    "EncodingProcessor",
    "FilterOperator",
    "DataFilteringProcessor",
    "StringOperationsProcessor",
    "CaseModifyingMethod",
    "DataCleanser",
    "MergeProcessor",
    "RowIdentifier",
    "RowSelector",
    "RowSorter",
]

# ------ method enums -------
from ._base import (
    CaseModifyingMethod,
    EncodingStrategies,
    FilterOperator,
    MissingValueStrategy,
    OutlierDetectionMethod,
)

# ----- Processors -----
from .data_cleansing import (
    DataCleanser,
    MissingValuesProcessor,
    OutliersProcessor,
    StringOperationsProcessor,
)
from .data_filtering import DataFilteringProcessor
from .data_prepare import DataPreparer
from .feature_engineering import (
    EncodingProcessor,
    FeatureSelection,
    MergeProcessor,
    NumericalInteractionFeatures,
)
from .row_ops import (
    RowIdentifier,
    RowSelector,
    RowSorter,
)
