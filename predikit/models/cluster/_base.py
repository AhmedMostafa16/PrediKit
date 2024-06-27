from abc import (
    ABC,
    abstractmethod,
)
from enum import StrEnum

from numpy import ndarray
from sklearn.base import (
    BaseEstimator,
    ClusterMixin,
)

from ..._typing import MatrixLike


class BaseCluster(ClusterMixin, BaseEstimator, ABC):
    """base class for all clusters."""

    @abstractmethod
    def fit(X: MatrixLike) -> "BaseCluster":
        pass

    @abstractmethod
    def fit_predict(X: MatrixLike) -> ndarray:
        pass


class ClusterStrategies(StrEnum):
    KMeans = "KMeans"
    DBSCAN = "DBSCAN"

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
            case "kmean" | "kmeans":
                return cls.KMeans
            case "dbscan":
                return cls.DBSCAN
            case _:
                raise ValueError(f"Invalid clustering strategy: {strategy}")
