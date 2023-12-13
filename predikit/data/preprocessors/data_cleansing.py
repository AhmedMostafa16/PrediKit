import logging
import numbers
from string import punctuation
from typing import (
    Self,
    override,
)

import numpy as np
from pandas import (
    DataFrame,
    Series,
)

from predikit.errors import (
    DataNotFittedError,
    NoNumericColumnsError,
    NoStringColumnsError,
)
from predikit.utils import (
    non_numeric_selector,
    numeric_columns_selector,
)

from ._base import (
    BasePreprocessor,
    CaseModifyingMethod,
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

        if self.fill_value is None or self.fill_value == "":
            if numeric_columns_selector(data) is not None:
                fill_value = 0
            else:
                fill_value = "missing_value"
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
    A preprocessor for detecting and handling outliers in a DataFrame.

    This class provides methods for fitting the processor to the data and
    transforming the data using the fitted operations. The outlier
    detection method and threshold can be specified during initialization.

    Attributes
    ----------
    method : OutlierDetectionMethod
        The method to use for outlier detection.
    threshold : float
        The threshold for determining outliers.
    add_indicator : bool
        Whether to add an indicator column for outliers in the transformed data.
    verbose : bool
        Whether to print verbose output.
    _weight : dict[str, tuple[float, float]]
        The weights calculated during fitting, used for transforming the data.
    """

    _weight: dict[str, tuple[float, float]]

    def __init__(
        self,
        method: OutlierDetectionMethod = OutlierDetectionMethod.IQR,
        threshold: float = 1.5,
        *,
        add_indicator: bool = False,
        verbose: bool = False,
    ) -> None:
        self.method = method
        self.threshold = threshold
        self.add_indicator = add_indicator
        self.verbose = verbose

    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
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
        else:
            columns = data.columns.tolist()

        if (selection := numeric_columns_selector(data, columns)) is None:
            raise NoNumericColumnsError(
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

            elif self.method == OutlierDetectionMethod.Z_SCORE:
                mean, std = self._fit_z_score(data, column)
                self._weight[column] = (mean, std)

                if not self.verbose:
                    continue

                filtered_samples = self._get_z_score(
                    mean, std, data, column, self.threshold
                )
                total_outliers = filtered_samples.sum()

            else:
                raise ValueError(
                    f"Wrong Outlier Detection Method {self.method}"
                )

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
        if self._weight == {}:
            raise DataNotFittedError(
                "Data must be fitted first using the 'fit' method"
            )

        for column in self._weight:
            if self.method == OutlierDetectionMethod.IQR:
                lower_bound, upper_bound = self._weight[column]
                outliers_mask = (data[column] < lower_bound) | (
                    data[column] > upper_bound
                )

                if self.add_indicator:
                    outlier_indicator = self._indicator_label(
                        column, self.method
                    )

                    data[outlier_indicator] = 0
                    data.loc[outliers_mask, outlier_indicator] = 1

                data.loc[data[column] < lower_bound, column] = lower_bound
                data.loc[data[column] > upper_bound, column] = upper_bound

            elif self.method == OutlierDetectionMethod.Z_SCORE:
                outliers_mask = self._get_z_score(
                    self._weight[column][0],
                    self._weight[column][1],
                    data,
                    column,
                    self.threshold,
                )

                if self.add_indicator:
                    outlier_indicator = self._indicator_label(
                        column, self.method
                    )

                    data[outlier_indicator] = 0
                    data.loc[outliers_mask, outlier_indicator] = 1

                data.loc[outliers_mask, column] = data[column].median()

            else:
                raise ValueError(
                    f"Wrong Outlier Detection Method {self.method}"
                )

        return data

    def _fit_z_score(
        self, data: DataFrame, column: str
    ) -> tuple[float, float]:
        """
        Calculates and returns the median and the Mean Absolute Deviation (MAD)
        of a specific column in a DataFrame.

        Parameters
        ----------
        data_frame : DataFrame
            The DataFrame containing the data.
        column_name : str
            The name of the column to calculate the median and MAD for.

        Returns
        -------
        tuple[float, float]
            A tuple containing the median and the MAD of the column.
        """
        column_median = data[column].median()
        column_mad = (data[column] - column_median).abs().median()
        return (column_median, column_mad)

    def _get_z_score(
        self,
        median: float,
        mad: float,
        data: DataFrame,
        column: str,
        threshold: float = 3.0,
    ) -> Series:
        """
        Calculates the modified Z-score for a specific column in a DataFrame
        and returns a boolean mask indicating which values are considered
        outliers based on the provided threshold.

        Parameters
        ----------
        median_value : float
            The median of the column.
        mad_value : float
            The Mean Absolute Deviation of the column.
        data_frame : DataFrame
            The DataFrame containing the data.
        column_name : str
            The name of the column to calculate the Z-score for.
        threshold : float, optional
            The threshold for determining outliers, by default 3.0

        Returns
        -------
        Series
            A boolean mask (Series of bool) indicating which values in the
            column are considered outliers.
        """
        scaling_factor = 0.7413
        z_scores = scaling_factor * ((data[column] - median) / mad)
        absolute_z_scores = z_scores.abs()
        outliers_mask = absolute_z_scores > threshold
        return outliers_mask

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
        Q1, Q3 = np.percentile(data[column], [25, 75])
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (lower_bound, upper_bound)

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

    def _indicator_label(
        self,
        column_name: str,
        method: OutlierDetectionMethod,
    ) -> str:
        return f"{column_name}_isOutlier_{method.name}"


class StringOperationsProcessor(BasePreprocessor):
    """
    A preprocessor for performing operations on string columns of a DataFrame.

    Attributes
    ----------
    case_modifier : CaseModifyingMethod or None
        The method to use for case modification.
    trim : bool
        Whether to trim leading and trailing whitespace.
    remove_whitespace : bool
        Whether to remove all whitespace.
    remove_numbers : bool
        Whether to remove all numeric characters.
    remove_letters : bool
        Whether to remove all alphabetic characters.
    remove_punctuation : bool
        Whether to remove all punctuation.
    verbose : bool
        Whether to print verbose output.
    """

    def __init__(
        self,
        case_modifier: CaseModifyingMethod | None = None,
        *,
        trim: bool = False,
        remove_whitespace: bool = False,
        remove_numbers: bool = False,
        remove_letters: bool = False,
        remove_punctuation: bool = False,
        verbose: bool = False,
    ):
        self.case_modifier = case_modifier
        self.trim = trim
        self.remove_whitespace = remove_whitespace
        self.remove_numbers = remove_numbers
        self.remove_letters = remove_letters
        self.remove_punctuation = remove_punctuation
        self.verbose = verbose

    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        """
        Fits the processor to the data.

        Parameters
        ----------
        data : DataFrame
            The data to fit.
        columns : list of str or None, optional
            The columns to fit. If None, all columns are used. Defaults to None.

        Returns
        -------
        Self
            The fitted processor.

        Raises
        ------
        NoStringColumnsError
            If no string columns are found in the data.
        """
        if columns:
            data = data[columns]

        self._str_data = non_numeric_selector(data, columns)

        if self._str_data is None:
            raise NoStringColumnsError(
                "No string columns found. "
                "StringModifierProcessor will be skipped."
            )

        self._operations = [
            (self.remove_punctuation, self._remove_punctuation),
            (self.remove_whitespace, self._remove_whitespace),
            (self.remove_numbers, self._remove_numbers),
            (self.remove_letters, self._remove_letters),
            (self.trim, self._trim),
            (self.case_modifier is not None, self._modify_case),
        ]

        return self

    def transform(self, data: DataFrame) -> DataFrame:
        """
        Transforms the data using the fitted operations.

        Parameters
        ----------
        data : DataFrame
            The data to transform.

        Returns
        -------
        DataFrame
            The transformed data.

        Raises
        ------
        ValueError
            If the data has not been fitted.
        DataNotFittedError
            If no string columns are found in the data.
        NoStringColumnsError
            If no operations are specified.
        """
        if not hasattr(self, "_str_data"):
            raise DataNotFittedError(
                "Data must be fitted first using the 'fit' method"
            )

        if self._str_data is None:
            raise DataNotFittedError(
                "No string columns found. "
                "StringModifierProcessor will be skipped."
            )

        if not self._operations:
            raise NoStringColumnsError("No string columns found.")

        for column in self._str_data.columns:
            for condition, operation in self._operations:
                if not condition:
                    continue
                operation(data, column)

        return data

    def _modify_case(self, data: DataFrame, column: str) -> DataFrame:
        """
        Modifies the case of the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to modify.
        column : str
            The column to modify.

        Returns
        -------
        DataFrame
            The modified data.

        Raises
        ------
        ValueError
            If an invalid case modifying method is specified.
        """
        if self.case_modifier == CaseModifyingMethod.UPPER:
            data[column] = data[column].str.upper()
        elif self.case_modifier == CaseModifyingMethod.LOWER:
            data[column] = data[column].str.lower()
        elif self.case_modifier == CaseModifyingMethod.TITLE:
            data[column] = data[column].str.title()
        elif self.case_modifier == CaseModifyingMethod.CAPITALIZE:
            data[column] = data[column].str.capitalize()
        elif self.case_modifier == CaseModifyingMethod.SWAPCASE:
            data[column] = data[column].str.swapcase()
        else:
            raise ValueError(
                f"Invalid Case Modifying Method {self.case_modifier}"
            )
        return data

    def _trim(self, data: DataFrame, column: str) -> DataFrame:
        """
        Trims leading and trailing whitespace from the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to trim.
        column : str
            The column to trim.

        Returns
        -------
        DataFrame
            The trimmed data.
        """
        data[column] = data[column].str.strip()
        return data

    def _remove_whitespace(self, data: DataFrame, column: str) -> DataFrame:
        """
        Removes all whitespace from the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to modify.
        column : str
            The column to modify.

        Returns
        -------
        DataFrame
            The modified data.
        """
        data[column] = data[column].str.replace(r"\s+", "", regex=True)
        return data

    def _remove_numbers(self, data: DataFrame, column: str) -> DataFrame:
        """
        Removes all numeric characters from the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to modify.
        column : str
            The column to modify.

        Returns
        -------
        DataFrame
            The modified data.
        """
        data[column].replace(r"\d+", "", regex=True, inplace=True)
        return data

    def _remove_letters(self, data: DataFrame, column: str) -> DataFrame:
        """
        Removes all alphabetic characters from the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to modify.
        column : str
            The column to modify.

        Returns
        -------
        DataFrame
            The modified data.
        """
        data[column].replace(r"[a-zA-Z]+", "", regex=True, inplace=True)
        return data

    def _remove_punctuation(self, data: DataFrame, column: str) -> DataFrame:
        """
        Removes all punctuation from the strings in the specified column of the data.

        Parameters
        ----------
        data : DataFrame
            The data to modify.
        column : str
            The column to modify.

        Returns
        -------
        DataFrame
            The modified data.
        """
        data[column] = data[column].apply(
            lambda x: "".join([char for char in x if char not in punctuation])
        )
        return data
