import logging
from typing import (
    Self,
    override,
)

from pandas import DataFrame

from . import (
    BasePreprocessor,
    CategoricalEncodingStrategies,
    Encoder,
)
from ._encoders import init_encoder


class FeatureSelection(BasePreprocessor):
    """_summary_

    Parameters
    ----------
    BasePreprocessor : _type_
        _description_
    """
    def __init__(self) -> None:
        self.stored_cols = None
        self.stored_dtypes = None

    @override
    def fit(
        self,
        data: DataFrame,
        cols: list[str] | None = None,
        dtypes: list[str] | None = None,
    ) -> Self:
        self.empty = False
        if cols is None and dtypes is None:
            self.empty = True
        elif cols is None and dtypes is not None:
            self.stored_dtypes = dtypes
            self.empty = False
        elif cols is not None and dtypes is None:
            self.stored_cols = cols
            self.empty = False
        else:
            self.stored_cols = cols
            self.stored_dtypes = dtypes
            self.empty = False

        return self

    @override
    def transform(
        self,
        data: DataFrame,
        cols: list[str] | None = None,
        dtypes: list[str] | None = None,
    ) -> DataFrame:
        if self.empty == True:
            return data
        else:
            if self.stored_cols is None and self.stored_dtypes is not None:
                data = data.select_dtypes(exclude=self.stored_dtypes)
            elif self.stored_cols is not None and self.stored_dtypes is None:
                data = data.loc[:, ~data.columns.isin(self.stored_cols)]
            else:
                data = data.loc[
                    :, ~data.columns.isin(self.stored_cols)
                ].select_dtypes(exclude=self.stored_dtypes)

        return data


class NumericalInteractionFeatures(BasePreprocessor):
    pass


class EncodingProcessor(BasePreprocessor):
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
    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        if columns is not None:
            data = data[columns]

        self._encoder = init_encoder(self.strategy, **self._encoder_params)
        self._encoder.fit(data)
        self.encoded_names = self._encoder.get_feature_names_out()

        if self.encoded_names.size == 0:
            logging.info("No columns to be encoded")

        return self

    @override
    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        masked_data = data[columns] if columns else data

        if self.encoded_names.size == 0:
            raise ValueError("No columns to be encoded")

        encoded_values = self._encoder.transform(masked_data)

        data[self.encoded_names] = encoded_values.toarray()

        if columns:
            data.drop(columns, axis=1, inplace=True)

        return data

    @override
    def fit_transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        self.fit(data, columns)
        return self.transform(data, columns)
