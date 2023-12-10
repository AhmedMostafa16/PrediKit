import logging
import numbers
from typing import Any, Self
from typing import override

import numpy as np
import pandas as pd

from . import (
    Cleaner,
    MissingValueStrategy,
    OutlierDetectionMethod,
)


class MissingValuesProcessor(Cleaner):
    """Processor for completing missing values with simple strategies.

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

    _cleaner_type: str = "MissingValues"

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
    def fit(self, data: pd.DataFrame, cols: list[str] | None = None) -> Self:
        """Fit the MissingValuesProcessor to the data.

        Parameters
        ----------
        data : pd.DataFrame
            dataset (pd.DataFrame shape = (n_samples, n_features))
        cols : list[str] | None, optional
            list of features to consider for fitting, by default None

        Returns
        -------
        self
            The fitted MissingValuesProcessor instance.
        """
        if cols is not None:
            data = data[cols]

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
            MissingValueStrategy.MEAN: pd.DataFrame.mean,
            MissingValueStrategy.MEDIAN: pd.DataFrame.median,
            MissingValueStrategy.MODE: pd.DataFrame.mode,
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
        self, data: pd.DataFrame, cols: list[str] | None = None
    ) -> pd.DataFrame:
        """Apply the MissingValuesProcessor to the dataset.

        Parameters
        ----------
        data : pd.DataFrame
            The input dataframe (shape = (n_samples, n_features)

        Returns
        -------
        pd.DataFrame
            The transformed dataframe (shape = (n_samples, n_features))
        """
        if cols is not None:
            data = data[cols]

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

    @override
    def fit_transform(
        self, data: pd.DataFrame, cols: list[str] | None = None
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        data : pd.DataFrame
            _description_
        cols : list[str] | None, optional
            _description_, by default None

        Returns
        -------
        pd.DataFrame
            _description_
        """
        self.fit(data, cols)  # Name
        return self.transform(data)  # Name Age Credit

    def _add_missing_value_indicator(
        self, data: pd.DataFrame, na_cols: list[str]
    ) -> pd.DataFrame:
        """
        Add indicator columns to a DataFrame to mark missing values.

        For each column name in `na_cols`, this method adds a new column to
        `data` with the suffix "_isNA".
        Each element in the new column is 1 if the corresponding element in the
        original column is NaN, and 0 otherwise.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame to which to add the indicator columns.
        na_cols : List[str]
            A list of column names for which to add indicator columns.

        Returns
        -------
        pd.DataFrame
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

    def _log_missing_percent(
        self, data: pd.DataFrame, threshold: float
    ) -> None:
        """
        Log the percentage of missing values in each column of a DataFrame.

        This function iterates over each column in the DataFrame, calculates
        the percentage of missing values in the column, and logs a warning if
        the percentage is greater than a specified threshold.

        Parameters
        ----------
        data : pd.DataFrame
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
        >>> df = pd.DataFrame({'A': [1, 2, np.nan], 'B': [4, np.nan, np.nan]})
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


class OutliersProcessor(Cleaner):
    """Class to process outliers in a dataset using a
    specified outlier detection method.

    Attributes
    ----------
    _cleaner_type : str
        "Outliers"

    Parameters
    ----------
    method : OutlierDetectionMethod
        The method to use for detecting outliers. Default is 'IQR'.
    threshold : float
        The threshold for the outlier detection method. Default is 1.5.

    Methods
    -------
    fit(data, cols)
        Fit the OutliersProcessor to the data.
    transform(data)
        Apply the OutliersProcessor to the data.
    _IQR(data, col, threshold)
        Outlier Detection using the Interquartile Range Rule.
    """

    _cleaner_type: str = "Outliers"
    _weights = {}

    def __init__(
        self,
        method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        threshold: float = 1.5,
    ) -> None:
        self.method = method
        self.threshold = threshold

    @override
    def fit(self, data: pd.DataFrame, cols: list[str]) -> Self:
        """Fit the OutliersProcessor on the dataset.

        Parameters
        ----------
        data : pd.DataFrame
            The dataset to fit on (shape = (n_samples, n_features)).
        cols : list[str]
            The columns to consider for fitting.

        Returns
        -------
        self
            The fitted OutliersProcessor instance.
        """
        raise NotImplementedError

    @override
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform the dataset by processing outliers.

        Parameters
        ----------
        data : pd.DataFrame
            The dataframe to transform (shape = (n_samples, n_features)).

        Returns
        -------
        pd.DataFrame
            The transformed dataframe (shape = (n_samples, n_features)).
        """
        raise NotImplementedError

    def _IQR(
        self, data: pd.DataFrame, col: str, threshold: float = 1.5
    ) -> tuple[float, float]:
        """Outlier Detection using the Interquartile Range Rule.
        Calculate Q3, Q1, IQR
        Q3: 75th quantile, Q1: 25th quantile
        IQR = Q3 - Q1
        Any value beyond:
            lower_bound = Q1 - (IQR * threshold)
            upper_bound = Q3 + (IQR * threshold)
        are regarded as outliers.


        Parameters
        ----------
        data : pd.DataFrame
            dataset (pd.DataFrame shape = (n_samples, n_features))
        col : str
            feature_name
        threshold : float, optional
            threshold on method, by default 1.5

        Returns
        -------
        tuple[float, float]
            lower_bound and upper_bound
        """
        q3, q1 = np.percentile(data[col], [75, 25])
        iqr = q3 - q1
        lower_bound = q1 - (iqr * threshold)
        upper_bound = q3 + (iqr * threshold)
        return (lower_bound, upper_bound)



