from abc import ABC
from abc import abstractmethod
from abc import abstractproperty
from enum import StrEnum
from enum import auto
from typing import Self
from numpy import ndarray

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder

class Preprocessor(TransformerMixin, BaseEstimator):
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
    >>> class CustomPreprocessor(Preprocessor):
    ...     def fit(self, X, y=None):
    ...         # Implement fit functionality here
    ...         return self
    ...
    ...     def transform(self, X):
    ...         # Implement transform functionality here
    ...         return X_transformed
    """
    
    pass


class Cleaner(Preprocessor, ABC):
    """The cleaner base class in data preprocessing.

    Parameters
    ----------
    method : StrEnum
        method used for cleaning the dataset
    """

    @abstractmethod
    def __init__(self, method: StrEnum, verbose: bool = False) -> None:
        pass

    @abstractmethod
    def fit(
        self,
        data: pd.DataFrame,
        cols: list[str] | None = None,
    ) -> Self:
        """Fit CleanOutliers / MissingValuesProcessor to the dataset.

        Parameters
        ----------
        data : pd.DataFrame
            dataset (pd.DataFrame shape = (n_samples, n_features))
        cols : list[str],
            list feature names to be cleaned

        Returns
        -------
        self
        """
        ...

    @abstractmethod
    def transform(
        self,
        data: pd.DataFrame,
        cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Transforms the dataset by cleaning the features.

        Parameters
        ----------
        data : pd.DataFrame
            dataset (pd.DataFrame shape = (n_samples, n_features))

        Returns
        -------
        pd.DataFrame
            dataset with the cleaned features
            (pd.DataFrame shape = (n_samples, n_features)
        """
        ...

    @abstractproperty
    def _cleaner_type(self) -> str:
        """Return the type of cleaner.

        Returns
        -------
        str
            type of cleaner
        """
        ...


class Encoder(Preprocessor, ABC):
    pass



class FeatureEngineering(Preprocessor, ABC):
    pass


class MissingValueStrategy(StrEnum):
    """Enum for specifying the method of handling missing values.

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


class OutlierDetectionMethod(StrEnum):
    """Enum for specifying the method of detecting outliers.

    Attributes
    ----------
    IQR : enum member
        Represents the Interquartile Range Rule
    Z_SCORE : enum member
        Represents the Z Score Rule
    """

    IQR = auto()
    Z_SCORE = auto()

class EncodingStrategies(StrEnum):
    pass

class CategoricalEncodingStrategies(EncodingStrategies):
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


class BinaryEncodingStrategies(EncodingStrategies):
    """
    Enum class for different types of binary encoding strategies.

    This class provides an enumeration of common binary
    encoding strategies. Each member of the enumeration
    represents a different type of binary encoder.

    Attributes
    ----------
    OrdinalEncoder : enum member
        Represents the Ordinal Encoder strategy.

    Examples
    --------
    >>> encoder = BinaryEncoderStrategies.OrdinalEncoder
    """

    OrdinalEncoder = auto()
