import logging
from typing import (
    Self,
    override,
)

from pandas import DataFrame

from predikit import util
from predikit.errors.transformer import DataNotFittedError

from .._typing import (
    FeatureType,
    MergeHow,
)
from ._base import (
    BasePreprocessor,
    Encoder,
    EncodingStrategies,
)
from ._encoders import init_encoder


class FeatureSelection(BasePreprocessor):
    def __init__(
        self,
        include_dtypes: list[FeatureType] | None = None,
        exclude_dtypes: list[FeatureType] | None = None,
        verbose: bool = False,
    ) -> None:
        self.include_dtypes: tuple[FeatureType, ...] = (
            tuple(include_dtypes) if include_dtypes else ()
        )
        self.exclude_dtypes: tuple[FeatureType, ...] = (
            tuple(exclude_dtypes) if exclude_dtypes else ()
        )
        self.verbose: bool = verbose

    def fit(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> Self:
        if columns:
            data = data[columns]
        else:
            columns = util.get_dataframe_column_names(data)

        selection = (
            frozenset(self.include_dtypes),
            frozenset(self.exclude_dtypes),
        )

        if not any(selection):
            raise ValueError(
                "at least one of include or exclude must be nonempty"
            )

        include_set = frozenset(self.include_dtypes)
        exclude_set = frozenset(self.exclude_dtypes)

        if not include_set.isdisjoint(exclude_set):
            raise ValueError(
                f"include and exclude overlaps on {include_set & exclude_set}"
            )

        selected_dtypes = list(include_set) or []

        if self.exclude_dtypes:
            if self.include_dtypes:
                selected_dtypes = list(include_set - exclude_set)
            else:
                selected_dtypes = util.exclude_from_columns(
                    util.get_distinct_columns_dtype(data), list(exclude_set)
                )

        self.selected_features = util.select_dtypes_columns(
            data, selected_dtypes
        )

        if self.verbose:
            logging.debug(selected_dtypes)
            logging.debug(self.selected_features)

        return self

    @override
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> DataFrame:
        if columns:
            data = data[columns]
        else:
            columns = util.get_dataframe_column_names(data)

        if not hasattr(self, "selected_features"):
            raise DataNotFittedError

        return data[self.selected_features]


class MergeProcessor(BasePreprocessor):
    """A class used to merge two DataFrames.
    Attributes
    ----------
    data : DataFrame
        The DataFrame to merge with.
    on : str | list[str]
        The column or columns to merge on.
    how : MergeHow
        The type of merge to perform.
    suffixes : tuple[str, str]
        The suffixes to add to the column names if they are the same in both
        DataFrames.
    """

    def __init__(
        self,
        data: DataFrame,
        on: str | list[str],
        how: MergeHow = "inner",
        suffixes: tuple[str, str] = ("_x", "_y"),
    ) -> None:
        self.data: DataFrame = data
        self.on: str | list[str] = on
        self.how: MergeHow = how
        self.suffixes: tuple[str, str] = suffixes

    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]

        # catch KeyError if `on` attribute column is not found
        return self.data.merge(
            right=data,
            on=self.on,
            how=self.how,
            suffixes=self.suffixes,
        )


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

    def fit(
        self,
        data: DataFrame,
    ) -> None:
        self._encoder.fit(data)

    @override
    def transform(
        self,
        data: DataFrame,
    ) -> DataFrame:
        return self._encoder.transform(data)

    def fit_transform(self, data: DataFrame) -> list[str]:
        return self._encoder.fit_transform(data)

    def get_feature_names_out(self):
        if self.strategy in [
            EncodingStrategies.OneHotEncoder,
        ]:
            return self._encoder.get_features_names_out()
        else:
            raise ValueError(
                "This Encoder does not support get_features_names_out."
            )
