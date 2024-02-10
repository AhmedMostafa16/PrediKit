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
    "BasicFilteringProcessor",
    "StringOperationsProcessor",
    "CaseModifyingMethod",
    "DataCleanser",
    "FeatureType",
]

# ------ method enums -------
from ._base import (
    CaseModifyingMethod,
    EncodingStrategies,
    FeatureType,
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
from .data_filtering import BasicFilteringProcessor
from .data_prepare import DataPreparer
from .feature_engineering import (
    EncodingProcessor,
    FeatureSelection,
    NumericalInteractionFeatures,
)
