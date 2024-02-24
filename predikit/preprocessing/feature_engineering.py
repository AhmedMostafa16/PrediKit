import logging
from typing import (
    Self,
    # override,
)
from xml.etree.ElementInclude import include

from pandas import DataFrame
from result import (
    Err,
    Ok,
    Result,
)

from ._base import (
    BasePreprocessor,
    Encoder,
    EncodingStrategies,
    FeatureType,
)
from ._encoders import init_encoder
from ._base import EncodingStrategies


class FeatureSelection(BasePreprocessor):
    """_summary_

    Parameters
    ----------
    BasePreprocessor : _type_
        _description_
    """

    def __init__(
        self,
        include_dtypes: list[FeatureType] | str | list[str] | None = None,
        exclude_dtypes: list[FeatureType] | str | list[str] | None = None,
        verbose: bool = False,
    ) -> None:
        self.include_dtypes = include_dtypes
        self.exclude_dtypes = exclude_dtypes
        self.verbose = verbose
        self.stored_cols = None
        self.stored_dtypes = None

    # ToDo: Add include/exclude dtypes parameter
    #@ override
    def fit(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> Self | Err[str]:
        # if columns and exclude:
        #     exc = ValueError(
        #         "Only one of 'columns' and 'exclude' can be specified"
        #     )
        # return Err(str(exc))
        if self.include_dtypes is not None:
            dtypes = None
            if isinstance(self.include_dtypes, str):
                dtypes = FeatureType.from_str(self.include_dtypes)
            elif isinstance(self.include_dtypes, list):
                if isinstance(self.include_dtypes[0], str):
                    dtypes = FeatureType.from_list(self.include_dtypes)
                else:
                    dtypes = list(self.include_dtypes)

            self.include_dtypes = dtypes

        self.empty = False
        if columns is None and self.exclude_dtypes is None:
            self.empty = True
        elif columns is None and self.exclude_dtypes is not None:
            self.stored_dtypes = self.exclude_dtypes
            self.empty = False
        elif columns is not None and self.exclude_dtypes is None:
            self.stored_cols = columns
            self.empty = False
        else:
            self.stored_cols = columns
            self.stored_dtypes = self.exclude_dtypes
            self.empty = False

        return self

    #@ override
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> Result[DataFrame, str]:
        if self.empty == True:
            exc = ValueError("No columns or dtypes to be selected")
            return Err(str(exc))
        else:
            if self.stored_cols is None and self.stored_dtypes is not None:
                data = data.select_dtypes(exclude=self.stored_dtypes)
            elif self.stored_cols is not None and self.stored_dtypes is None:
                data = data.loc[:, ~data.columns.isin(self.stored_cols)]
            else:
                data = data.loc[
                    :, ~data.columns.isin(self.stored_cols)
                ].select_dtypes(exclude=self.stored_dtypes)

        if data.empty:
            exc = ValueError("This results in an empty data frame")
            return Err(str(exc))

        return Ok(data)


class NumericalInteractionFeatures(BasePreprocessor):
    pass


class EncodingProcessor(BasePreprocessor):
    _encoder: Encoder

    def __init__(
        self,
        strategy: EncodingStrategies = EncodingStrategies.OneHotEncoder,
        *,
        verbose: bool = False,
        **encoder_params,
    ) -> None:
        self.verbose = verbose
        self.strategy = strategy
        self._encoder_params = encoder_params
        self._encoder = init_encoder(strategy, **encoder_params)

    #@ override
    def fit(self, data: DataFrame, 
            ) -> None:
        self._encoder.fit(data)

    #@ override
    def transform(
        self, data: DataFrame, 
    ) -> Result[DataFrame, str]:
        return self._encoder.transform(data)

    def fit_transform(self, data: DataFrame) -> list[str]:
        return self._encoder.fit_transform(data)

    def get_feature_names_out(self):
        if self.strategy in [EncodingStrategies.OneHotEncoder,]:
            return self._encoder.get_features_names_out()
        else:
            raise ValueError('This Encoder does not support get_features_names_out.')
