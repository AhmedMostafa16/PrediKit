from abc import (
    ABC,
    abstractmethod,
)
from enum import (
    Enum,
    StrEnum,
    auto,
)
from typing import (
    Callable,
    Self,
    override,
)

import numpy as np
from pandas import DataFrame
from scipy.sparse import csr_matrix
from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
)


class BasePreprocessor(TransformerMixin, BaseEstimator, ABC):
    """
    Base class for all preprocessing tasks in the data pipeline.

    This class inherits from both `TransformerMixin` and `BaseEstimator` from
    scikit-learn, providing a foundation for creating custom preprocessing
    steps. `TransformerMixin` provides the `fit_transform` method, which fits
    the model and returns the transformed data. `BaseEstimator` provides the
    `get_params` and `set_params` methods for handling estimator parameters.

    Note: This class should be used as a base class when creating new
    preprocessing steps. It should not be instantiated directly.

    Examples
    --------
    >>> class CustomPreprocessor(BasePreprocessor):
    >>>     def fit(self, data, columns=None):
    ...         # Implement fit functionality here
    ...         return self

    >>>     def transform(self, data):
    ...         # Implement transform functionality here
    ...         return X_transformed
    """

    def __init__(self, data: DataFrame, *args, **params):
        self.data = data

    def fit(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> Self:
        """
        Fit the preprocessing transformer to the given data.

        Parameters:
            data (DataFrame): The input data to fit the transformer on.
            columns (list[str] | None): Optional. The subset of columns to fit the transformer on.
                                        If None, all columns will be used.

        Returns:
            Self: The fitted transformer if successful, otherwise an error message.
        """
        return self

    @abstractmethod
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> DataFrame:
        """
        Apply the transformation to the given data.

        Args:
            data (DataFrame): The input data to be transformed.
            columns (list[str] | None, optional): The columns to be transformed. If None, all columns will be transformed. Defaults to None.

        Returns:
            DataFrame: The transformed data if successful, otherwise an error message.
        """
        ...

    def fit_transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
        **fit_params,
    ) -> DataFrame:
        """
        Fit the transformer to the data and transform it.

        Parameters:
            data (DataFrame): The input data to fit and transform.
            columns (list[str] | None, optional): The columns to apply the transformation on. If None, all columns are transformed. Defaults to None.
            **fit_params: Additional parameters to be passed to the fit method.

        Returns:
            DataFrame: The transformed data if successful, otherwise an error message.

        Raises:
            ValueError: If the input data is empty.
        """
        if data.empty:
            raise ValueError(
                "Dataset cannot be empty in fit_transform process."
            )

        if not columns:
            result = self.fit(data, **fit_params)
            return result.transform(data)

        result = self.fit(data, columns, **fit_params)
        return result.transform(data)


class Encoder(BasePreprocessor, ABC):
    @abstractmethod
    def get_feature_names_out(self) -> np.ndarray:
        """
        Return the names of the encoded features.

        Returns
        -------
        np.ndarray
            names of the encoded features
        """

    @override
    def transform(self, X) -> csr_matrix: ...


class MissingValueStrategy(StrEnum):
    """
    Enum for specifying the method of handling missing values.

    Attributes
    ----------
    MEAN : enum member
        Represents the mean imputation strategy
    MEDIAN : enum member
        Represents the median imputation strategy
    MODE : enum member
        Represents the mode imputation strategy
    CONSTANT : enum member
        Represents the constant imputation strategy
    OMIT : enum member
        Represents the omit imputation strategy
    """

    MEAN = auto()
    MEDIAN = auto()
    MODE = auto()
    CONSTANT = auto()
    OMIT = auto()

    @classmethod
    def from_str(cls, strategy: str) -> "MissingValueStrategy":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        MissingValueStrategy
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "mean":
                return cls.MEAN
            case "median":
                return cls.MEDIAN
            case "mode" | "most_frequent" | "most frequent" | "most-frequent":
                return cls.MODE
            case "constant" | "fill" | "value":
                return cls.CONSTANT
            # fmt: off
            case "omit" | "drop" | "dropna" | "drop_na" | "drop na" | "drop-na":
                return cls.OMIT
            # fmt: on
            case _:
                raise ValueError(
                    f"Invalid missing value handling strategy: {strategy}"
                )


class OutlierDetectionMethod(StrEnum):
    """
    Enum for specifying the method of detecting outliers.

    Attributes
    ----------
    IQR : enum member
        Represents the Interquartile Range Rule
    Z_SCORE : enum member
        Represents the Z Score Rule
    """

    IQR = auto()
    Z_SCORE = auto()

    @classmethod
    def from_str(cls, method: str) -> "OutlierDetectionMethod":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        method : str
            The string representation of the method.

        Returns
        -------
        OutlierDetectionMethod
            The enumeration member corresponding to the given string.
        """
        method = method.lower()
        match method:
            # fmt: off
            case (
                "iqr"
                | "interquartile_range"
                | "interquartile range"
                | "inter quartile range"
                | "inter quartile_range"
                | "inter quartile"
            ):
                return cls.IQR
            # fmt: on
            case "z_score" | "zscore" | "z-score" | "z":
                return cls.Z_SCORE
            case _:
                raise ValueError(
                    f"Invalid outlier detection method: {method}",
                )


class EncodingStrategies(StrEnum):
    """
    Enum class for different types of categorical encoders.

    This class provides an enumeration of common categorical
    encoding strategies. Each member of the enumeration
    represents a different type of categorical encoder.

    Attributes
    ----------
    HashingEncoder : enum member
        Represents the Hashing Encoder strategy.
    SumEncoder : enum member
        Represents the Sum Encoder strategy.
    BackwardDifferenceEncoder : enum member
        Represents the Backward Difference Encoder strategy.
    OneHotEncoder : enum member
        Represents the One Hot Encoder strategy.
    HelmertEncoder : enum member
        Represents the Helmert Encoder strategy.
    BaseNEncoder : enum member
        Represents the Base N Encoder strategy.
    CountEncoder : enum member
        Represents the Count Encoder strategy.

    Examples
    --------
    >>> encoder = CategoricalEncodingStrategies.OneHotEncoder
    """

    HashingEncoder = "HashingEncoder"
    SumEncoder = "SumEncoder"
    BackwardDifferenceEncoder = "BackwardDifferenceEncoder"
    OneHotEncoder = "OneHotEncoder"
    HelmertEncoder = "HelmertEncoder"
    BaseNEncoder = "BaseNEncoder"
    CountEncoder = "CountEncoder"
    LabelEncoder = "LabelEncoder"
    PolynomialEncoder = "PolynomialEncoder"
    OrdinalEncoder = "OrdinalEncoder"

    @classmethod
    def from_str(cls, strategy: str) -> "EncodingStrategies":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        EncodingStrategies
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "hashing" | "hashingencoder":
                return cls.HashingEncoder
            case "sum" | "sumencoder":
                return cls.SumEncoder
            # fmt: off
            case (
                "backward_difference"
                | "backwarddifference"
                | "backwarddifferenceencoder"
            ):
                return cls.BackwardDifferenceEncoder
            # fmt: on
            case "one_hot" | "onehot" | "onehotencoder":
                return cls.OneHotEncoder
            case "helmert" | "helmertencoder":
                return cls.HelmertEncoder
            case "base_n" | "basen" | "basenencoder":
                return cls.BaseNEncoder
            case "count" | "countencoder":
                return cls.CountEncoder
            case "label" | "labelencoder":
                return cls.LabelEncoder
            case "polynomial" | "polynomialencoder":
                return cls.PolynomialEncoder
            case "ordinal" | "ordinalencoder":
                return cls.OrdinalEncoder
            case _:
                raise ValueError(f"Invalid encoding strategy: {strategy}")


class FilterOperator(StrEnum):
    """
    An enumeration representing various filter operators used in
    data filtering.
    """

    EQUAL = auto()
    NOTEQUAL = auto()
    GREATER = auto()
    GREATEREQUAL = auto()
    LESS = auto()
    LESSEQUAL = auto()
    NULL = auto()
    NOTNULL = auto()
    CONTAINS = auto()
    DOES_NOT_CONTAIN = auto()

    @property
    def to_str(self) -> str:
        """
        Returns the string representation of the operator.

        Returns
        -------
        str
            The string representation of the operator.
        """

        return {
            FilterOperator.EQUAL: "==",
            FilterOperator.NOTEQUAL: "!=",
            FilterOperator.GREATER: ">",
            FilterOperator.GREATEREQUAL: ">=",
            FilterOperator.LESS: "<",
            FilterOperator.LESSEQUAL: "<=",
            FilterOperator.NULL: "isna",
            FilterOperator.NOTNULL: "notna",
            FilterOperator.CONTAINS: "in",
            FilterOperator.DOES_NOT_CONTAIN: "not in",
        }[self]

    @property
    def is_comparison_operator(self) -> bool:
        """
        Returns True if the operator is a comparison operator.

        Returns
        -------
        bool
            True if the operator is a comparison operator.
        """

        return self.value in self.tolist()[:6]

    @property
    def is_nullity_operator(self) -> bool:
        """
        Returns True if the operator is a null operator.

        Returns
        -------
        bool
            True if the operator is a null operator.
        """

        return self.value in self.tolist()[6:8]

    @property
    def is_containment_operator(self) -> bool:
        """
        Returns True if the operator is a contains operator.

        Returns
        -------
        bool
            True if the operator is a contains operator.
        """

        return self.value in self.tolist()[8:]

    @classmethod
    def from_str(cls, operator: str) -> "FilterOperator":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        operator : str
            The string representation of the operator.

        Returns
        -------
        FilterOperator
            The enumeration member corresponding to the given string.
        """
        operator = operator.lower()
        match operator:
            case "==" | "=" | "equal" | "equals" | "eq":
                return cls.EQUAL
            case "!=" | "ne" | "not_equal" | "notequal":
                return cls.NOTEQUAL
            case ">" | "gt" | "greater":
                return cls.GREATER
            case ">=" | "ge" | "greater_equal" | "greaterequal":
                return cls.GREATEREQUAL
            case "<" | "lt" | "less":
                return cls.LESS
            case "<=" | "le" | "less_equal" | "lessequal":
                return cls.LESSEQUAL
            case "isna" | "null":
                return cls.NULL
            case "notna" | "not_null" | "notnull":
                return cls.NOTNULL
            case "contains" | "in":
                return cls.CONTAINS
            case "does_not_contain" | "not in" | "dnc" | "doesnotcontain":
                return cls.DOES_NOT_CONTAIN
            case _:
                raise ValueError(f"Invalid filter operator: {operator}")

    def tolist(self):
        """
        Returns a list of all the members of the enumeration.

        Returns
        -------
        list
            A list of all the members of the enumeration.
        """
        return list(map(lambda c: c.value, self.__class__))


class CaseModifyingMethod(StrEnum):
    """
    An enumeration of methods for modifying the case of strings in a
    pandas Series.

    Attributes
    ----------
    LOWER : enum.auto
        Converts all characters to lowercase.
    UPPER : enum.auto
        Converts all characters to uppercase.
    TITLE : enum.auto
        Converts first character of each word to uppercase and remaining
        to lowercase.
    CAPITALIZE : enum.auto
        Converts first character to uppercase and remaining to lowercase.
    SWAPCASE : enum.auto
        Converts uppercase to lowercase and lowercase to uppercase.
    CASEFOLD : enum.auto
        Removes all case distinctions in the string.
    """

    LOWER = auto()
    UPPER = auto()
    TITLE = auto()
    CAPITALIZE = auto()
    SWAPCASE = auto()
    CASEFOLD = auto()

    @classmethod
    def from_str(cls, method: str) -> "CaseModifyingMethod":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        method : str
            The string representation of the method.

        Returns
        -------
        CaseModifyingMethod
            The enumeration member corresponding to the given string.
        """
        method = method.lower()
        match method:
            case "lower":
                return cls.LOWER
            case "upper":
                return cls.UPPER
            case "title":
                return cls.TITLE
            case "capitalize":
                return cls.CAPITALIZE
            case "swapcase":
                return cls.SWAPCASE
            case "casefold":
                return cls.CASEFOLD
            case _:
                raise ValueError(f"Invalid case modifying method: {method}")


class SelectionForm(Enum):
    """The selection form of the Row Selection Interpreter.

    Attributes
    ----------
    SINGLE : enum member
        A single digit returns only the entered row.
        >>> 5
    RANGE : enum member
        A range of numbers returns the rows in the range,
        including the entered rows.
        >>> 17-20
    TO : enum member
        A minus sign before a number returns first through the entered row.
        >>> -2
    FROM : enum member
        A number followed by a plus sign returns the entered row through the
        last row.
        >>> 5+
    """

    SINGLE = auto()
    RANGE = auto()
    TO = auto()
    FROM = auto()


class RowSelectionInterpreter:
    """
    Interpreting the input digits and signs to Row Selector Node

    Ranges to Return: Enter the rows or range of rows to return.

    A single digit returns only the entered row.
    For example, 3 returns only row 3.

    A minus sign before a number returns row 1 through the entered row.
    For example, -2 returns rows 1 and 2.

    A range of numbers returns the rows in the range,
    including the entered rows.
    For example, 17-20 returns rows 17, 18, 19, and 20.

    A number followed by a plus sign returns the entered row through the
    last row. For example, 50+ returns row 50 through the last row.

    Any combination can be used at the same time by entering
    the numbers on a new line.

    Attributes
    ----------
    input : str
        The special form input string to interpret.
    total_rows : int
        The total number of rows in the dataset.
    zero_indexed : bool
        Whether the rows are zero-indexed or not.
    _FORM_TO_OPERATION : dict[SelectionForm, Callable]
        A dictionary that maps the selection form to the operation to be
        performed on the selected rows.
    """

    def __init__(
        self,
        input: str,
        total_rows: int,
        *,
        zero_indexed: bool = False,
        delimiter: str | None = None,
    ) -> None:
        self.input: str = input
        self.length: int = total_rows
        self._selected_rows: set[int] = set()
        self.zero_indexed: bool = zero_indexed

        self._FORM_TO_OPERATION: dict[SelectionForm, Callable] = {
            SelectionForm.SINGLE: self._add_single_row,
            SelectionForm.FROM: self._add_rows_from,
            SelectionForm.TO: self._add_rows_to,
            SelectionForm.RANGE: self._add_row_range,
        }
        self.delimiter = delimiter

    def interpret(self) -> list[int]:
        """Interprets string input to a list of numbers that can be used to
        select indices from a DataFrame.

        Returns
        -------
        list[int]
            The sorted numbers to be used to select rows from a DataFrame.
        """
        for line in self.input.split(sep=self.delimiter):
            self._validate_and_interpret_line(line.strip())

        return sorted(self._selected_rows)

    def _get_digit_and_form(
        self, line: str
    ) -> tuple[int, SelectionForm] | tuple[tuple[int, int], SelectionForm]:
        """Extracts the digit and the form of the line.

        Parameters
        ----------
        line : str
            the original input form of the line.

        Returns
        -------
        tuple[int, SelectionForm]
            The digit extracted from the form of the line.
        tuple[tuple[int, int], SelectionForm]
            The range of digits extracted from the form of the line.
        """
        if line.isdigit():
            digit = self._adjust_index(int(line))
            return (digit, SelectionForm.SINGLE)
        elif self._is_plus(line):
            digit = self._adjust_index(int(line[:-1]))
            return (digit, SelectionForm.FROM)
        elif self._is_minus(line):
            digit = self._adjust_index(int(line[1:]))
            return (digit, SelectionForm.TO)
        elif self._is_range(line):
            lower, upper = map(int, line.split("-"))
            lower = self._adjust_index(lower)
            upper = self._adjust_index(upper)
            if lower > upper:
                lower, upper = upper, lower
            return (lower, upper), SelectionForm.RANGE

        raise ValueError(f"Unknown form `{line}`")

    def _validate_and_interpret_line(self, line: str) -> None:
        """Validates the line form then interprets it to the digits to be added
        to the row selection set `_selected_rows`.

        Parameters
        ----------
        line : str
            the original input form of the line.

        Raises
        ------
        ValueError
            Arises when the line doesn't match any of the supported forms.
        """
        digit, form = self._get_digit_and_form(line)
        self._validate_digit_in_range(line, digit)
        self._FORM_TO_OPERATION[form](digit)

    def _validate_digit_in_range(
        self, line: str, digit: int | tuple[int, int]
    ) -> None:
        """A validator function to check whether the digits from a line
        is inside the range of dataset length (0-N) where N is Length

        Parameters
        ----------
        digit : int | tuple[int, int]
            the digit or range of digits extracted from the entered form
        line : str
            in the original form entered by the user

        Examples
        --------
            >>> 1
            >>> -2
            >>> 5+
            >>> 2-5

        Raises
        ------
        ValueError
            Shows on which digit & in which line responsible for out of range
            error
        """
        digits = [digit] if isinstance(digit, int) else list(digit)
        for digit in digits:
            if not self._in_range(digit):
                correct_range: str = (
                    f"(0-{self.length - 1})"
                    if self.zero_indexed
                    else f"(1-{self.length})"
                )
                if not self.zero_indexed:
                    digit += 1
                raise ValueError(
                    f"Digit {digit} of line `{line}` is out of your dataset "
                    f"range, please pick a number between {correct_range}"
                )

    def _is_minus(self, input: str) -> bool:
        """Checks whether the input form abides to _add_rows_to method

        Examples
        --------
        >>> -2
        >>> -5
        >>> -(N-1)
        Where N is equal to the length of the dataset

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        return input.startswith("-") and self._is_integer(input[1:])

    def _is_plus(self, input: str) -> bool:
        """Checks whether the input form abides to _add_rows_to method

        Examples
        --------
        >>> 2+
        >>> 5+
        >>> Z+
        where 0 <= Z < N

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        return input.endswith("+") and self._is_integer(input[:-1])

    def _is_range(self, input: str) -> bool:
        """Checks whether the input form abides to _add_row_range method

        Examples
        --------
        >>> 17-20

        Parameters
        ----------
        input : str
            the original input from user input line

        Returns
        -------
        bool
            True if it falls under the noted form
            False otherwise
        """
        if "-" not in input or input.count("-") > 1:
            return False

        l, r = input.split("-")
        return self._is_integer(l) and self._is_integer(r)

    def _in_range(self, *digits: int) -> bool:
        """Checks whether the digit is in range of the dataset

        Returns
        -------
        bool
            True if digit is greater than and equal 0
            and less than dataset length
            False otherwise
        """
        return all(0 <= digit < self.length for digit in digits)

    def _add_single_row(self, digit: int) -> None:
        """Adds a single row to the selected rows.

        Parameters
        ----------
        digit : int
            The row number to add.
        """
        self._selected_rows.add(digit)

    def _add_rows_to(self, digit: int) -> None:
        """Adds all rows from the first row to the specified row.

        Examples
        --------
        >>> -2 => {0, 1, 2}
        >>> -5 => {0, 1, 2, 3, 4, 5}

        Parameters
        ----------
        digit : int
            The last row number to add.
        """
        self._selected_rows.update(range(0, digit + 1))

    def _add_rows_from(self, digit: int) -> None:
        """Adds all rows from the specified row to the last row.

        Examples
        --------
        >>> 50+ => {50, 51, 52, ....., N-1}

        Parameters
        ----------
        digit : int
            The first row number to add.
        """
        self._selected_rows.update(range(digit, self.length))

    def _add_row_range(self, rng: tuple[int, int]) -> None:
        """Adds all rows in the specified range.

        Examples
        --------
        >>> 17-20 => {17, 18, 19, 20}

        Parameters
        ----------
        lower : int
            The first row number in the range.
        upper : int
            The last row number in the range.
        """
        lower, upper = rng
        self._selected_rows.update(range(lower, upper + 1))

    def _is_integer(self, input: str) -> bool:
        """Checks whether the input can be converted to an integer."""
        return input.isdigit()

    def _adjust_index(self, digit: int) -> int:
        """Adjusts the digit index to zero or one indexed."""
        return digit - (not self.zero_indexed)
