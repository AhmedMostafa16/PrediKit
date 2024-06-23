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
from predikit.util import (
    get_dataframe_column_names,
    get_non_numeric_data,
    get_numeric_data,
    select_numeric_columns,
)
from predikit.util.data_utils import exclude_from_columns

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

    Attributes
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

    Examples
    --------
    >>> import pandas as pd
    >>> from predikit import MissingValuesProcessor
    >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [1, 2, np.nan, 4, 5]})

    >>> mvp = MissingValuesProcessor()
    >>> cleaned_X_train = mvp.fit_transform(df)
    >>> cleaned_X_test = mvp.transform(df)
    >>> df
    """

    def __init__(
        self,
        *,
        strategy: MissingValueStrategy | str = MissingValueStrategy.MEAN,
        fill_value: str | int | float | None = None,
        add_indicator: bool = False,
        verbose: bool = False,
    ) -> None:
        self.strategy = strategy
        self.fill_value = fill_value
        self.add_indicator = add_indicator
        self.verbose = verbose

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
        if columns:
            data = data[columns]

        if isinstance(self.strategy, str):
            self.strategy = MissingValueStrategy.from_str(self.strategy)

        if self.strategy not in (
            MissingValueStrategy.CONSTANT,
            MissingValueStrategy.OMIT,
            MissingValueStrategy.MODE,
        ):
            if (num_data := get_numeric_data(data)) is None:
                raise NoNumericColumnsError(
                    "Selected columns are of non-numeric type. "
                    "Unable to process missing values on non-numeric columns."
                    f" When using {self.strategy} strategy, only numeric "
                    "columns are allowed."
                )

            data = num_data

        if self.verbose:
            self._log_missing_percent(data, threshold=0.25)

        if self.fill_value is None:
            if select_numeric_columns(data) is not None:
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
                f"'fill_value'={fill_value} is invalid. Expected a "
                "numerical value when imputing numerical data"
            )

        self.na_cols = data.columns[data.isna().any()].tolist()

        if not self.na_cols:
            logging.debug("No missing values in features.")
            return self

        strategy_fill = {
            MissingValueStrategy.MEAN: DataFrame.mean,
            MissingValueStrategy.MEDIAN: DataFrame.median,
            MissingValueStrategy.MODE: DataFrame.mode,
            MissingValueStrategy.CONSTANT: lambda _: fill_value,
            MissingValueStrategy.OMIT: lambda _: None,
        }

        if self.strategy == MissingValueStrategy.MODE:
            self.fill_value = strategy_fill[self.strategy](
                data[self.na_cols]
            ).iloc[0]
        else:
            self.fill_value = strategy_fill[self.strategy](data[self.na_cols])

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
        if columns:
            data = data[columns]

        if not hasattr(self, "na_cols"):
            raise DataNotFittedError

        if not self.na_cols:
            return data

        if self.strategy != MissingValueStrategy.OMIT and self.add_indicator:
            self._add_missing_value_indicator(data, self.na_cols)

        if self.strategy == MissingValueStrategy.OMIT:
            self._omit_missing_values(data, self.na_cols)
        else:
            data[self.na_cols] = self._fill_missing_values(data[self.na_cols])

        return data

    def _fill_missing_values(self, data: DataFrame) -> DataFrame:
        data = data.fillna(value=self.fill_value)
        return data

    def _omit_missing_values(
        self, data: DataFrame, columns: list[str]
    ) -> None:
        data.dropna(subset=columns, inplace=True)

    def _missing_value_label(self, column: str) -> str:
        return column + "_isNA"

    def _missing_value_labels(self, columns: list[str]) -> list[str]:
        return [self._missing_value_label(col) for col in columns]

    def _add_missing_value_indicator(
        self, data: DataFrame, na_cols: list[str]
    ) -> DataFrame:
        """
        Add indicator columns to a DataFrame to mark missing values.

        For each column name in `na_cols`, this method adds a new column to
        `data` with the suffix "_isNA".
        Each element in the new column is 1 if the corresponding element in
        the original column is NaN, and 0 otherwise.

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

            label = self._missing_value_label(na_col)
            data[label] = data[na_col].isna().astype("uint8")

        return data

    def _log_missing_percent(self, data: DataFrame, threshold: float) -> None:
        """
        Log the percentage of missing values in each column of a DataFrame.

        This function iterates over each column in the DataFrame, calculates
        the percentage of missing values in the column, and logs a warning
        if the percentage is greater than a specified threshold.

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
        ... _log_missing_percent(df, 0.5)
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
        Whether to add an indicator column for outliers in the transformed
        data.
    verbose : bool
        Whether to print verbose output.
    _weight : dict[str, tuple[float, float]]
        The weights calculated during fitting, used for transforming the data.
    """

    _weight: dict[str, tuple[float, float]]

    def __init__(
        self,
        method: OutlierDetectionMethod | str = OutlierDetectionMethod.IQR,
        threshold: float = 1.5,
        *,
        add_indicator: bool = True,
        verbose: bool = False,
    ) -> None:
        self.method = method
        self.threshold = threshold
        self.add_indicator = add_indicator
        self.verbose = verbose

    def fit(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> Self:
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
            columns = get_dataframe_column_names(data)

        if (selection := select_numeric_columns(data, columns)) is None:
            raise NoNumericColumnsError(
                "Selected columns are of non-numeric type."
                "Unable to process outliers on non-numeric columns."
            )

        numeric_notna_columns = [s for s in selection if data[s].notna().all()]

        if not numeric_notna_columns:
            raise ValueError(
                "All numeric columns has missing values, can't "
                "process outliers, skipping Outliers Processing... "
                "You should run the Missing Values Processor first."
            )

        if isinstance(self.method, str):
            self.method = OutlierDetectionMethod.from_str(self.method)

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

            else:
                mean, std = self._fit_z_score(data, column)
                self._weight[column] = (mean, std)

                if not self.verbose:
                    continue

                filtered_samples = self._get_z_score(
                    mean, std, data, column, self.threshold
                )
                total_outliers = filtered_samples.sum()

            if self.verbose:
                if total_outliers <= 0:
                    continue
                self._log_outliers_num_percent(total_outliers, data, column)

        return self

    @override
    def transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
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
        if not hasattr(self, "_weight") or self._weight == {}:
            raise DataNotFittedError

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
        logging.debug(
            f"Number of outliers detected: {outliers_num} in Feature {column}"
        )

        logging.debug(
            "Proportion of outlier detected: {}%".format(
                round((100 / (len(data) / outliers_num)), 1)
            )
        )

    def _indicator_label(
        self,
        column_name: str,
        method: OutlierDetectionMethod | str,
    ) -> str:
        return f"{column_name}_isOutlier_{method.upper()}"


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
        case_modifier: CaseModifyingMethod | str | None = None,
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
            The columns to fit. If None, all columns are used.
            Defaults to None.

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

        self._str_data = get_non_numeric_data(data, columns)

        if self._str_data is None:
            exc = NoStringColumnsError(
                "No string columns found. "
                "StringModifierProcessor will be skipped."
            )

            raise exc

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
            raise DataNotFittedError

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
        """
        data[column] = getattr(data[column].str, str(self.case_modifier))()

        return data

    def _trim(self, data: DataFrame, column: str) -> DataFrame:
        """
        Trims leading and trailing whitespace from the strings in the
        specified column of the data.

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
        Removes all whitespace from the strings in the specified column of
        the data.

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
        Removes all numeric characters from the strings in the specified
        column of the data.

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
        Removes all alphabetic characters from the strings in the specified
        column of the data.

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
        Removes all punctuation from the strings in the specified
        column of the data.

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


class DataCleanser(BasePreprocessor):
    """
    A class used to clean data by handling missing values, outliers,
    and string operations.

    Attributes
    ----------
    missing_value_handler : MissingValuesProcessor, optional
        An instance of MissingValuesProcessor to handle missing values
        in the data.
    outlier_handler : OutliersProcessor, optional
        An instance of OutliersProcessor to handle outliers in the data.
    string_operator : StringOperationsProcessor, optional
        An instance of StringOperationsProcessor to perform string operations
        on the data.
    is_fitted : bool
        A flag indicating whether the cleaner has been fitted.
    """

    _clean_missing_enc: MissingValuesProcessor | None = None
    _clean_outliers_enc: OutliersProcessor | None = None
    _string_operations_enc: StringOperationsProcessor | None = None
    _fitted: bool = False

    # ToDos
    # [x] Missing Values Handling
    # [x] Outliers Detection and Treatment
    # [x] String Operations
    # [ ] Standardization & Normalization
    # [ ] Duplication Handling
    # [ ] Inconsistent Data Handling
    # [ ] Validation & Sanity checks of Data
    def __init__(
        self,
        missing_clean: bool = True,
        missing_strategy: (
            MissingValueStrategy | str
        ) = MissingValueStrategy.MEAN,
        missing_fill_value: int | float | str | None = None,
        missing_indicator: bool = False,
        outlier_clean: bool = True,
        outlier_method: (
            OutlierDetectionMethod | str
        ) = OutlierDetectionMethod.IQR,
        outlier_threshold: float = 2.5,
        outlier_indicator: bool = True,
        str_operations: bool = False,
        str_case_modifier_method: CaseModifyingMethod | str | None = None,
        str_trim: bool = False,
        str_remove_whitespace: bool = False,
        str_remove_numbers: bool = False,
        str_remove_letters: bool = False,
        str_remove_punctuation: bool = False,
        verbose: bool = False,
    ) -> None:
        self.verbose = verbose
        self.clean_missing = missing_clean
        self.clean_strategy = missing_strategy
        self.fill_value = missing_fill_value
        self.missing_indicator = missing_indicator
        self.outlier_indicator = outlier_indicator
        self.clean_outliers = outlier_clean
        self.outliers_method = outlier_method
        self.outliers_threshold = outlier_threshold
        self.string_operations = str_operations
        self.case_modifier = str_case_modifier_method
        self.trim = str_trim
        self.remove_whitespace = str_remove_whitespace
        self.remove_numbers = str_remove_numbers
        self.remove_letters = str_remove_letters
        self.remove_punctuation = str_remove_punctuation

    def fit(self, data: DataFrame, columns: list[str] | None = None) -> Self:
        raise TypeError("Use the 'fit_transform' method instead of 'fit'")

    @override
    def fit_transform(
        self, data: DataFrame, columns: list[str] | None = None
    ) -> DataFrame:
        if columns:
            data = data[columns]
        else:
            columns = get_dataframe_column_names(data)

        if self.clean_missing:
            cme = self._clean_missing_enc = MissingValuesProcessor(
                strategy=self.clean_strategy,
                fill_value=self.fill_value,
                add_indicator=self.missing_indicator,
                verbose=self.verbose,
            )
            logging.debug("> Cleansing")
            data = cme.fit_transform(data)

        if self.clean_outliers:
            coe = self._clean_outliers_enc = OutliersProcessor(
                method=self.outliers_method,
                threshold=self.outliers_threshold,
                add_indicator=self.outlier_indicator,
                verbose=self.verbose,
            )
            logging.debug("> Outliers")
            missing_labels = None

            # ToDo optimize this to be created while creating labels
            if self._clean_missing_enc is not None and self.missing_indicator:
                logging.debug("Post-cleansing column correction")
                na_cols = self._clean_missing_enc.na_cols
                # undesired for outliers detection and treatment
                missing_labels = self._clean_missing_enc._missing_value_labels(
                    na_cols
                )

            na_cols = exclude_from_columns(columns, missing_labels)
            data = coe.fit_transform(data, columns=na_cols)

        if self.string_operations:
            soe = self._string_operations_enc = StringOperationsProcessor(
                case_modifier=self.case_modifier,
                trim=self.trim,
                remove_whitespace=self.remove_whitespace,
                remove_numbers=self.remove_numbers,
                remove_letters=self.remove_letters,
                remove_punctuation=self.remove_punctuation,
                verbose=self.verbose,
            )
            logging.debug("> String Operations")
            data = soe.fit_transform(data)

        self._fitted = True
        return data

    @override
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> DataFrame:
        if not self._fitted:
            raise DataNotFittedError(
                "Data must be fitted first using the 'fit_transform' method"
            )

        if columns:
            data = data[columns]

        if self._clean_missing_enc:
            logging.debug("> Cleansing")
            data = self._clean_missing_enc.transform(data)

        if self._clean_outliers_enc:
            logging.debug("> Outliers")
            data = self._clean_outliers_enc.transform(data)

        if self._string_operations_enc:
            logging.debug("> String Operations")
            data = self._string_operations_enc.transform(data)

        return data
