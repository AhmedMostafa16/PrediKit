from ._base import BaseCluster, ClusterStrategies
from numpy import ndarray
from typing import Any
from ..._typing import MatrixLike
from sklearn.exceptions import NotFittedError

from sklearn.cluster import DBSCAN, KMeans


class Cluster(BaseCluster):
    """
    A class that encapsulates various clustering algorithms for efficient data analysis.
    ### Parameters
    strategy : {"KMeans", "DBSCAN"}, default= None

    params: a dictionary of parameters {'parameter': value -> (str, int or float)}.
    """

    _CLUSTERS: dict[ClusterStrategies, Any] = {
        ClusterStrategies.DBSCAN: DBSCAN,
        ClusterStrategies.KMeans: KMeans,
    }

    def __init__(
        self,
        strategy: ClusterStrategies = None,
        params: dict[str, str | int | float] = None,
    ) -> None:
        if strategy is None:
            raise ValueError("Select a Cluster.")
        else:
            self.strategy = ClusterStrategies.from_str(strategy)

        if params is None:
            self.model = self._CLUSTERS[self.strategy]()
        else:
            self.model = self._CLUSTERS[self.strategy](**params)

    def fit(self, X: MatrixLike) -> "Cluster":
        """
        Fits the cluster model to the input data `X`.

        Args:
            X: The input data to be used for training.

        Returns:
            Cluster: The `Cluster` object.
        """
        return self.model.fit(X)

    def predict(self) -> ndarray:
        """
        Returns:
            ndarray: An array of predicted labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.labels_
        except:
            raise NotFittedError("You have to fit the model first.")

    def fit_predict(self, X: MatrixLike) -> ndarray:
        """
        Fits the cluster model to the input data `X`.

        Args:
            X: The input data to be used for training.

        Returns:
            ndarray: An array of cluster labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        return self.model.fit_predict(X)

    def get_labels(self) -> ndarray:
        """
        Returns:
            ndarray: An array of cluster labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.labels_
        except:
            raise NotFittedError("You have to fit the model first.")

    def get_inertia(self) -> float:
        """
        Calculates the within-cluster inertia.

        Returns:
            float: Calculated inertia.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        if self.strategy is ClusterStrategies.KMeans:
            try:
                return self.model.labels_
            except:
                raise NotFittedError("You have to fit the model first.")
        else:
            raise ValueError("This model does not support get_inertia.")

    def get_centroids(self) -> ndarray:
        """
        Retrieves the cluster centroids (means).

        Returns:
            ndarray: An array of centroids.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        if self.strategy is ClusterStrategies.KMeans:
            try:
                return self.model.cluster_centers_
            except:
                raise NotFittedError("You have to fit the model first.")
        else:
            raise ValueError("This model does not support get_centroids.")
