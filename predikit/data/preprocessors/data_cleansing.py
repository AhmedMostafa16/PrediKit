import logging
import numbers
from typing import (
    Self,
    override,
)

import numpy as np
from pandas import DataFrame

from ._base import (
    BasePreprocessor,
    MissingValueStrategy,
    OutlierDetectionMethod,
)


class MissingValuesProcessor(BasePreprocessor):
    """
    Processor for completing missing values with simple strategies.

    Replace missing values using a descriptive statistic (e.g. mean, median,or
    most frequent) along each column, or using a constant value, or omitting.

    Parameters
    ----------
    strategy : MissingValueStrategy, default='MEAN'
        The processor strategy.

        - MEAN: replace missing values using the mean along
            each column. Can only be used with numeric data.
        - MEDIAN: replace missing values using the median along
            each column. Can only be used with numeric data.
        - MODE: replace missing using the most frequent
            value along each column. Can be used with strings or numeric data.
        - CONSTANT: replace missing values with fill_value. Can be
            used with strings or numeric data.
        - OMIT: drop rows with missing values. Can be
            used with strings or numeric data.

    fill_value : str or numerical value, default=None
        When strategy == "constant", `fill_value` is used to replace all
        occurrences of missing_values. For string or object data types,
        `fill_value` must be a string.
        If `None`, `fill_value` will be 0 when imputing numerical
        data and "missing_value" for strings or object data types.

    add_indicator : bool, default=False
        If True, a boolean indicator column is added to the DataFrame
        to denote missing values. The default is False.

    verbose : bool, default=False
        If True, prints information about missing values in the dataset.

    Attributes
    ----------
    method : MissingValuesStrategy
        The strategy to use for handling missing values. Default is 'MEDIAN'.

    Examples
    --------
    >>> import pandas as pd
    >>> from predikit import MissingValuesProcessor
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [1, 2, np.nan, 4, 5]})
    >>>
    >>> mvp = MissingValuesProcessor()
    >>> cleaned_X_train = mvp.fit_transform(df)
    >>> cleaned_X_test = mvp.transform(df)
    >>> df
    """

    def __init__(
        self,
        *,
        strategy: MissingValueStrategy = MissingValueStrategy.MEAN,
        fill_value: str | int | float | None = None,
        add_indicator: bool = False,
        verbose: bool = False,
    ) -> None:
        self.strategy = strategy
        self.fill_value = fill_value
        self.add_indicator = add_indicator
        self.verbose = verbose

    @override
    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        """
        Fit the MissingValuesProcessor to the data.

        Parameters
        ----------
        data : DataFrame
            dataset (DataFrame shape = (n_samples, n_features))
        columns : list[str] | None, optional
            list of features to consider for fitting, by default None

        Returns
        -------
        self
            The fitted MissingValuesProcessor instance.
        """
        if columns is not None:
            data = data[columns]

        if self.strategy not in (
            MissingValueStrategy.CONSTANT,
            MissingValueStrategy.OMIT,
            MissingValueStrategy.MODE,
        ):
            data = data.select_dtypes(include="number")

        if self.verbose:
            self._log_missing_percent(data, threshold=0.25)

        if self.fill_value is None:
            if data.dtypes.apply(lambda x: x.kind in ("u", "i", "f")).all():
                fill_value = 0
            else:
                fill_value = "missing_values"
        else:
            fill_value = self.fill_value

        # fill_value should be numerical in case of numerical input
        if (
            self.strategy == MissingValueStrategy.CONSTANT
            and data.dtypes.apply(lambda x: x.kind in ("u", "i", "f")).all()
            and not isinstance(fill_value, numbers.Real)
        ):
            raise ValueError(
                "'fill_value'={0} is invalid. Expected a "
                "numerical value when imputing numerical "
                "data".format(fill_value)
            )

        self.na_cols = data.columns[data.isna().any()].tolist()

        if not self.na_cols:
            logging.info("No missing values in features.")

        strategy_fill = {
            MissingValueStrategy.MEAN: DataFrame.mean,
            MissingValueStrategy.MEDIAN: DataFrame.median,
            MissingValueStrategy.MODE: DataFrame.mode,
            MissingValueStrategy.CONSTANT: lambda _: fill_value,
            MissingValueStrategy.OMIT: lambda _: None,
        }

        try:
            self.fill_value = strategy_fill[self.strategy](data)
        except KeyError:
            raise ValueError(f"Invalid strategy: {self.strategy}")

        return self

    @override
    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        """
        Apply the MissingValuesProcessor to the dataset.

        Parameters
        ----------
        data : DataFrame
            The input dataframe (shape = (n_samples, n_features)

        Returns
        -------
        DataFrame
            The transformed dataframe (shape = (n_samples, n_features))
        """
        if columns is not None:
            data = data[columns]

        if not self.na_cols:
            raise ValueError("No missing values in features.")

        if self.strategy != MissingValueStrategy.OMIT and self.add_indicator:
            self._add_missing_value_indicator(data, self.na_cols)

        # omit
        if self.fill_value is None:
            data.dropna(inplace=True)
        else:
            data.fillna(self.fill_value, inplace=True)

        return data

    def _add_missing_value_indicator(
        self, data: DataFrame, na_cols: list[str]
    ) -> DataFrame:
        """
        Add indicator columns to a DataFrame to mark missing values.

        For each column name in `na_cols`, this method adds a new column to
        `data` with the suffix "_isNA".
        Each element in the new column is 1 if the corresponding element in the
        original column is NaN, and 0 otherwise.

        Parameters
        ----------
        data : DataFrame
            The DataFrame to which to add the indicator columns.
        na_cols : List[str]
            A list of column names for which to add indicator columns.

        Returns
        -------
        DataFrame
            The DataFrame with the added indicator columns.

        Raises
        ------
        ValueError
            If `na_cols` contains a column name that is not in `data`.
        """
        for na_col in na_cols:
            if na_col not in data.columns:
                raise ValueError(
                    f"Column {na_col} does not exist in the DataFrame."
                )
            data[na_col + "_isNA"] = data[na_col].isna().astype("uint8")

        return data

    def _log_missing_percent(self, data: DataFrame, threshold: float) -> None:
        """
        Log the percentage of missing values in each column of a DataFrame.

        This function iterates over each column in the DataFrame, calculates
        the percentage of missing values in the column, and logs a warning if
        the percentage is greater than a specified threshold.

        Parameters
        ----------
        data : DataFrame
            The DataFrame for which to log the percentage of missing values.
        threshold : float
            The threshold percentage for logging a warning. If the percentage
            of missing values in a column is greater than this threshold,
            a warning is logged.

        Returns
        -------
        None

        Examples
        --------
        >>> df = DataFrame({'A': [1, 2, np.nan], 'B': [4, np.nan, np.nan]})
        >>> _log_missing_percent(df, 0.5)
        Warning: ! Attention B - 67% Missing!
        """
        for col in data.columns:
            pct_missing = data[col].isnull().mean()
            if pct_missing > threshold:
                logging.warning(
                    "! Attention {} - {}% Missing!".format(
                        col, round(pct_missing * 100)
                    )
                )


class OutliersProcessor(BasePreprocessor):
    """
    Class to process outliers in a dataset using a
    specified outlier detection method.

    Attributes
    ----------
    _weight : dict
        holds the weight of the Outlier Procecssor method

    Parameters
    ----------
    method : OutlierDetectionMethod
        The method to use for detecting outliers. Default is 'IQR'.
    threshold : float
        The threshold for the outlier detection method. Default is 1.5.

    Methods
    -------
    fit(data, columns)
        Fit the OutliersProcessor to the data.
    transform(data)
        Apply the OutliersProcessor to the data.
    _IQR(data, column, threshold)
        Outlier Detection using the Interquartile Range Rule.
    """

    _weight: dict

    def __init__(
        self,
        method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        threshold: float = 1.5,
        verbose: bool = False,
    ) -> None:
        self.method = method
        self.threshold = threshold
        self.verbose = verbose

    def fit(self, data: DataFrame, columns: list[str]) -> Self:
        """
        Fit the OutliersProcessor on the dataset.

        Parameters
        ----------
        data : DataFrame
            The dataset to fit on (shape = (n_samples, n_features)).
        columns : list[str]
            The columns to consider for fitting.

        Returns
        -------
        self
            The fitted OutliersProcessor instance.
        """
        if columns:
            data = data[columns]

        if (selection := self._numeric_selector(data, columns)) == []:
            raise ValueError(
                "Selected columns are of non-numeric type. "
                "Unable to process outliers on non-numeric columns."
            )

        data = data[selection]
        self._weight = {}
        for column in selection:
            if self.method == OutlierDetectionMethod.IQR:
                lower_bound, upper_bound = self._IQR(
                    data, column, self.threshold
                )
                self._weight[column] = (lower_bound, upper_bound)

                if not self.verbose:
                    continue

                total_outliers = len(
                    data[column][
                        (data[column] < lower_bound)
                        | (data[column] > upper_bound)
                    ]
                )

            # bug not detecting outliers correctly
            elif self.method == OutlierDetectionMethod.Z_SCORE:
                mean, std = self._fit_z_score(data, column)
                self._weight[column] = [mean, std]

                if not self.verbose:
                    continue

                filtered_samples = self._get_z_score(
                    mean, std, data, column, self.threshold
                )
                total_outliers = filtered_samples.sum()

            else:
                raise ValueError("Wrong Outlier Detection Method")

            if self.verbose:
                if total_outliers <= 0:
                    continue
                self._log_outliers_num_percent(total_outliers, data, column)

        return self

    @override
    def transform(self, data: DataFrame) -> DataFrame:
        """
        Transform the dataset by processing outliers.

        Parameters
        ----------
        data : DataFrame
            The dataframe to transform (shape = (n_samples, n_features)).

        Returns
        -------
        DataFrame
            The transformed dataframe (shape = (n_samples, n_features)).
        """
        if self.method == OutlierDetectionMethod.IQR:
            pass

        return data

    def _fit_z_score(
        self, data: DataFrame, column: str
    ) -> tuple[float, float]:
        mean = data[column].mean()
        std = data[column].std()
        return (mean, std)

    def _get_z_score(
        self,
        mean: float,
        std: float,
        data: DataFrame,
        column: str,
        threshold: float = 3,
    ):
        return np.abs(((data[column] - mean) / std)) > threshold

    def _IQR(
        self,
        data: DataFrame,
        column: str,
        threshold: float = 1.5,
    ) -> tuple[float, float]:
        """
        Outlier Detection using the Interquartile Range Rule.
        Calculate Q3, Q1, IQR
        Q3: 75th quantile, Q1: 25th quantile
        IQR = Q3 - Q1
        Any value beyond:
            lower_bound = Q1 - (IQR * threshold)
            upper_bound = Q3 + (IQR * threshold)
        are regarded as outliers.


        Parameters
        ----------
        data : DataFrame
            dataset (DataFrame shape = (n_samples, n_features))
        column : str
            feature_name
        threshold : float, optional
            threshold on method, by default 1.5

        Returns
        -------
        tuple[float, float]
            lower_bound and upper_bound
        """
        q3, q1 = np.percentile(data[column], [75, 25])
        iqr = q3 - q1
        lower_bound = q1 - (iqr * threshold)
        upper_bound = q3 + (iqr * threshold)
        return (lower_bound, upper_bound)

    def _numeric_selector(
        self, data: DataFrame, columns: list[str]
    ) -> list[str]:
        numeric_columns = []
        for col in columns:
            if data[col].dtype.kind not in "iuf":
                continue
            numeric_columns.append(col)

        return numeric_columns

    def _log_outliers_num_percent(
        self, outliers_num: int, data: DataFrame, column: str
    ) -> None:
        logging.info(
            f"Number of outliers detected: {outliers_num} in Feature {column}"
        )

        logging.info(
            "Proportion of outlier detected: {}%".format(
                round((100 / (len(data) / outliers_num)), 1)
            )
        )
