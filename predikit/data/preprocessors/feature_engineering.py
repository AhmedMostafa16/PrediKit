import logging
from typing import (
    Self,
    override,
)

from pandas import DataFrame

from . import (
    CategoricalEncodingStrategies,
    Encoder,
    Preprocessor,
)
from ._encoders import init_encoder


class FeatureSelection(Preprocessor):
    pass


class NumericalInteractionFeatures(Preprocessor):
    pass


class EncodingProcessor(Preprocessor):
    _encoder: Encoder

    def __init__(
        self,
        strategy: CategoricalEncodingStrategies = CategoricalEncodingStrategies.OneHotEncoder,
        *,
        verbose: bool = False,
        **encoder_params,
    ) -> None:
        self.verbose = verbose
        self.strategy = strategy
        self._encoder_params = encoder_params

    @override
    def fit(self, data: DataFrame, cols: list[str] | None = None) -> Self:
        if cols is not None:
            data = data[cols]

        self._encoder = init_encoder(self.strategy, **self._encoder_params)
        self._encoder.fit(data)
        self.encoded_names = self._encoder.get_feature_names_out()

        if self.encoded_names.size == 0:
            logging.info("No columns to be encoded")

        return self

    @override
    def transform(
        self, data: DataFrame, cols: list[str] | None = None
    ) -> DataFrame:
        masked_data = data[cols] if cols else data

        if self.encoded_names.size == 0:
            raise ValueError("No columns to be encoded")

        encoded_values = self._encoder.transform(masked_data)

        data[self.encoded_names] = encoded_values.toarray()

        if cols:
            data.drop(cols, axis=1, inplace=True)

        return data

    @override
    def fit_transform(
        self, data: DataFrame, cols: list[str] | None = None
    ) -> DataFrame:
        self.fit(data, cols)
        return self.transform(data, cols)
