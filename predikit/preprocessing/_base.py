from abc import (
    ABC,
    abstractmethod,
)
from enum import (
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
    ...     def fit(self, data, columns=None):
    ...         # Implement fit functionality here
    ...         return self
    ...
    ...     def transform(self, data):
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
            case "notna()" | "not_null" | "notnull":
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


class FeatureType(StrEnum):
    INTEGER = "i"
    FLOAT = "f"
    BOOLEAN = "b"
    DATETIME = "M"
    TIMEDELTA = "m"
    CATEGORY = "O"
    OBJECT = "O"

    @classmethod
    def from_str(cls, dtype: str) -> "FeatureType":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        dtype : str
            The string representation of the dtype.

        Returns
        -------
        FeatureType
            The enumeration member corresponding to the given string.
        """
        dtype = dtype.lower()
        match dtype:
            case "int" | "int64" | "int32" | "int16" | "int8" | "integer":
                return cls.INTEGER
            case "float" | "float64" | "float32" | "float16":
                return cls.FLOAT
            case "bool" | "boolean":
                return cls.BOOLEAN
            case "datetime" | "datetime64" | "datetime32" | "datetime16":
                return cls.DATETIME
            case "timedelta" | "timedelta64" | "timedelta32" | "timedelta16":
                return cls.TIMEDELTA
            case "category":
                return cls.CATEGORY
            case "object" | "str" | "string":
                return cls.OBJECT
            case _:
                raise ValueError(f"Invalid dtype: {dtype}")

    @classmethod
    def from_list(cls, dtypes: list[str]) -> list["FeatureType"]:
        """
        Returns a list of enumeration members corresponding to the given
        list of strings.

        Parameters
        ----------
        dtypes : list[str]
            The list of string representations of the dtypes.

        Returns
        -------
        list[FeatureType]
            A list of enumeration members corresponding to the given list
            of strings.
        """
        return list(map(cls.from_str, dtypes))

    def list(self):
        """
        Returns a list of all the members of the enumeration.

        Returns
        -------
        list
            A list of all the members of the enumeration.
        """

        return list(map(lambda c: c.value, self.__class__))
