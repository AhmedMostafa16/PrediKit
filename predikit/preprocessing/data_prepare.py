"""This module is responsible for automating the whole preprocessing proces for AutoML."""
import logging

import pandas as pd

from ._base import (
    BasePreprocessor,
    Encoder,
    EncodingStrategies,
    MissingValueStrategy,
    OutlierDetectionMethod,
)
from .data_cleansing import (
    MissingValuesProcessor,
    OutliersProcessor,
)


class DataPreparer(BasePreprocessor):
    _clean_missing_enc: MissingValuesProcessor | None = None
    _clean_outliers_enc: OutliersProcessor | None = None
    _encoder: Encoder | None = None
    _binary_encoder: Encoder | None = None
    _fitted: bool = False

    # ToDo: add support for replacing values
    def __init__(
        self,
        clean_missing: bool = True,
        clean_strategy: MissingValueStrategy = MissingValueStrategy.MEAN,
        fill_value: str | None = None,
        clean_outliers: bool = True,
        outliers_method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        clean_indicator: bool = False,
        outliers_threshold: float = 1.5,
        cat_encoders_strategies: list[EncodingStrategies] = None,
        drop_invariant: bool = False,
        normalization: bool = False,
        random_state: int = 42,
        verbose: bool = False,
    ) -> None:
        if cat_encoders_strategies is None:
            cat_encoders_strategies = [
                EncodingStrategies.HelmertEncoder,
                EncodingStrategies.CountEncoder,
            ]
        self.verbose = verbose
        self.cat_encoders_strategies = cat_encoders_strategies
        self.random_state = random_state

        self._clean_missing = clean_missing
        self._clean_strategy = clean_strategy
        self._fill_value = fill_value
        self._clean_indicator = clean_indicator
        self._clean_outliers = clean_outliers
        self._outliers_method = outliers_method
        self._outliers_threshold = outliers_threshold
        self._drop_invariant = drop_invariant
        self._normalization = normalization

    def fit_transform(
        self,
        data: pd.DataFrame,
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        logging.debug("#" * 50)
        logging.debug("! START Preprocessing Data")
        if self._clean_missing:
            self._clean_missing_enc = MissingValuesProcessor(
                strategy=self._clean_strategy,
                add_indicator=self._clean_indicator,
                fill_value=None,
                verbose=self.verbose,
            )
            logging.debug("> Cleansing")
            data = self._clean_missing_enc.fit_transform(data, columns)

        return data

    def transform(
        self, data: pd.DataFrame, columns: list[str] | None = None
    ) -> pd.DataFrame:
        if self._clean_missing_enc:
            logging.debug("> Cleansing")
            data = self._clean_missing_enc.transform(data, columns)

        return data
