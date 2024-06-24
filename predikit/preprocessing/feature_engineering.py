from typing import (
    Self,
    override,
)

from pandas import DataFrame

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
        self.include_dtypes = include_dtypes
        self.exclude_dtypes = exclude_dtypes
        self.verbose = verbose
        self.stored_cols = None
        self.stored_dtypes = None

    # ToDo: Add include/exclude dtypes parameter
    @override
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
    @override
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> DataFrame:
        if self.empty is True:
            raise ValueError("No columns or dtypes to be selected")
        else:
            if self.stored_cols is None and self.stored_dtypes is not None:
                data = data.select_dtypes(exclude=self.stored_dtypes)
            elif self.stored_cols is not None and self.stored_dtypes is None:
                data = data.loc[:, ~data.columns.isin(self.stored_cols)]
            else:
                data = data.loc[:, ~data.columns.isin(self.stored_cols)].select_dtypes(
                    exclude=self.stored_dtypes
                )

        if data.empty:
            raise ValueError("This results in an empty data frame")

        return data


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

    @override
    def fit(
        self,
        data: DataFrame,
    ) -> None:
        self._encoder.fit(data)

    @override
    @override
    def transform(
        self,
        data: DataFrame,
    ) -> DataFrame:
    ) -> DataFrame:
        return self._encoder.transform(data)

    def fit_transform(self, data: DataFrame) -> list[str]:
        return self._encoder.fit_transform(data)

    def get_feature_names_out(self):
        if self.strategy in [
            EncodingStrategies.OneHotEncoder,
        ]:
            return self._encoder.get_features_names_out()
        raise ValueError("This Encoder does not support get_features_names_out.")
