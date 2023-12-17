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
    ...     def fit(self, X, y=None):
    ...         # Implement fit functionality here
    ...         return self
    ...
    ...     def transform(self, X):
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
        ...

    @abstractmethod
    def transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
    ) -> DataFrame:
        ...

    def fit_transform(
        self,
        data: DataFrame,
        columns: list[str] | None = None,
        **fit_params,
    ) -> DataFrame:
        if not columns:
            return self.fit(data, **fit_params).transform(data)

        return self.fit(data, columns, **fit_params).transform(data)


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
    def transform(self, X) -> csr_matrix:
        ...


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
    def from_str(cls, strategy: str) -> Self:
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
                return MissingValueStrategy.MEAN
            case "median":
                return MissingValueStrategy.MEDIAN
            case "mode" | "most_frequent" | "most frequent" | "most-frequent":
                return MissingValueStrategy.MODE
            case "constant" | "fill" | "value":
                return MissingValueStrategy.CONSTANT
            case "omit" | "drop" | "dropna" | "drop_na" | "drop na" | "drop-na":
                return MissingValueStrategy.OMIT
            case _:
                raise ValueError(f"Invalid missing value strategy: {strategy}")


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
    def from_str(cls, method: str) -> Self:
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
            case "iqr" | "interquartile_range" | "interquartile range" | "inter quartile range" | "inter quartile_range" | "inter quartile":
                return OutlierDetectionMethod.IQR
            case "z_score" | "zscore" | "z-score" | "z":
                return OutlierDetectionMethod.Z_SCORE
            case _:
                raise ValueError(f"Invalid outlier detection method: {method}")


class CategoricalEncodingStrategies(Enum):
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

    HashingEncoder = auto()
    SumEncoder = auto()
    BackwardDifferenceEncoder = auto()
    OneHotEncoder = auto()
    HelmertEncoder = auto()
    BaseNEncoder = auto()
    CountEncoder = auto()
    LabelEncoder = auto()
    PolynomialEncoder = auto()
    OrdinalEncoder = auto()


class FilterOperator(StrEnum):
    """
    An enumeration representing various filter operators used in data filtering.
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
            FilterOperator.NULL: "isna()",
            FilterOperator.NOTNULL: "notna()",
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

        return self.value in self.list()[:6]

    @property
    def is_nullity_operator(self) -> bool:
        """
        Returns True if the operator is a null operator.

        Returns
        -------
        bool
            True if the operator is a null operator.
        """

        return self.value in self.list()[6:8]

    @property
    def is_containment_operator(self) -> bool:
        """
        Returns True if the operator is a contains operator.

        Returns
        -------
        bool
            True if the operator is a contains operator.
        """

        return self.value in self.list()[8:]

    def list(self):
        """
        Returns a list of all the members of the enumeration.

        Returns
        -------
        list
            A list of all the members of the enumeration.
        """

        return list(map(lambda c: c.value, self.__class__))

    @classmethod
    def from_str(cls, operator: str) -> Self:
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
            case "==" | "=" | "equal" | "eq":
                return FilterOperator.EQUAL
            case "!=" | "ne" | "not_equal":
                return FilterOperator.NOTEQUAL
            case ">" | "gt" | "greater":
                return FilterOperator.GREATER
            case ">=" | "ge" | "greater_equal":
                return FilterOperator.GREATEREQUAL
            case "<" | "lt" | "less":
                return FilterOperator.LESS
            case "<=" | "le" | "less_equal":
                return FilterOperator.LESSEQUAL
            case "isna" | "null":
                return FilterOperator.NULL
            case "notna()" | "not_null":
                return FilterOperator.NOTNULL
            case "contains" | "in":
                return FilterOperator.CONTAINS
            case "does_not_contain" | "not in":
                return FilterOperator.DOES_NOT_CONTAIN
            case _:
                raise ValueError(f"Invalid filter operator: {operator}")


class CaseModifyingMethod(StrEnum):
    """
    An enumeration of methods for modifying the case of strings in a pandas Series.

    Attributes
    ----------
    LOWER : enum.auto
        Converts all characters to lowercase.
    UPPER : enum.auto
        Converts all characters to uppercase.
    TITLE : enum.auto
        Converts first character of each word to uppercase and remaining to lowercase.
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
