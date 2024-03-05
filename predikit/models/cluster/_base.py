from abc import(
    ABC, 
    abstractmethod
)

from enum import StrEnum

from sklearn.base import (
    ClusterMixin,
    BaseEstimator
)
from typing import Any
from ..._typing import DataFrame, Series

class BaseCluster(ClusterMixin, BaseEstimator, ABC):

    @abstractmethod
    def fit_predict(X: DataFrame, Y: Series) -> Any:
        pass

class ClusterStrategies(StrEnum):

    KMeans = 'KMeans'
    DBSCAN = 'DBSCAN'

    @classmethod
    def from_str(cls, strategy: str) -> "ClusterStrategies":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        ClusterStrategies
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "kmean" | 'kmeans':
                return cls.KMeans
            case "dbscan":
                return cls.DBSCAN
            case _:
                raise ValueError(f"Invalid clustering strategy: {strategy}")