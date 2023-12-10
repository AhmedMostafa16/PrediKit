from ._base import (
    BinaryEncodingStrategies,
    CategoricalEncodingStrategies,
    FeatureEngineering,
)

type EncodingStrategies = BinaryEncodingStrategies | CategoricalEncodingStrategies


class FeatureSelection(FeatureEngineering):
    pass


class NumericalInteractionFeatures(FeatureEngineering):
    pass
