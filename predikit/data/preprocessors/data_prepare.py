import logging

import pandas as pd

from predikit.data.preprocessors.data_cleansing import (
    MissingValuesProcessor,
    OutliersProcessor,
)

from . import (
    CategoricalEncodingStrategies,
    Encoder,
    MissingValueStrategy,
    OutlierDetectionMethod,
    Preprocessor,
)


class DataPrepare(Preprocessor):
    _clean_missing_enc: MissingValuesProcessor
    _clean_outliers_enc: OutliersProcessor
    _encoder: Encoder
    _binary_encoder: Encoder

    # ToDo: add support for replacing values
    def __init__(
        self,
        clean_missing: bool = True,
        clean_strategy: MissingValueStrategy = MissingValueStrategy.MEAN,
        clean_outliers: bool = True,
        clean_indicator: bool = False,
        outliers_method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        outliers_threshold: float = 1.5,
        cat_encoders_strategies: list[CategoricalEncodingStrategies] = [
            CategoricalEncodingStrategies.HelmertEncoder,
            CategoricalEncodingStrategies.CountEncoder,
        ],
        drop_invariant: bool = False,
        normalization: bool = False,
        random_state: int = 42,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        self.cat_encoders_strategies = cat_encoders_strategies
        self.random_state = random_state

        self._clean_missing = clean_missing
        self._clean_strategy = clean_strategy
        self._clean_indicator = clean_indicator
        self._clean_outliers = clean_outliers
        self._outliers_method = outliers_method
        self._outliers_threshold = outliers_threshold
        self._drop_invariant = drop_invariant
        self._normalization = normalization

    def fit_transform(
        self,
        data: pd.DataFrame,
        cols: list[str] | None = None,
    ) -> pd.DataFrame:
        logging.info("#" * 50)
        logging.info("! START Preprocessing Data")
        if self._clean_missing:
            self._clean_missing_enc = MissingValuesProcessor(
                strategy=self._clean_strategy,
                add_indicator=self._clean_indicator,
                fill_value=None,
                verbose=self.verbose,
            )
            logging.info("> Cleansing")
            data = self._clean_missing_enc.fit_transform(data, cols)

        return data

    def transform(
        self, data: pd.DataFrame, cols: list[str] | None = None
    ) -> pd.DataFrame:
        if self._clean_missing_enc:
            logging.info("> Cleansing")
            data = self._clean_missing_enc.transform(data, cols)

        return data

    def run(self):
        pass
