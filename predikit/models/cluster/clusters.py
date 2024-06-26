from typing import Any

from numpy import ndarray
from pandas import DataFrame
from sklearn.cluster import (
    DBSCAN,
    KMeans,
)
from sklearn.exceptions import NotFittedError

from ._base import (
    BaseCluster,
    ClusterStrategies,
)


class Cluster(BaseCluster):
    """
    A class that encapsulates various clustering algorithms for efficient data analysis.

    Parameters:
        strategy (str): The clustering strategy to be used. Valid options are "KMeans" and "DBSCAN".
        data (DataFrame): The input data for clustering.
        cols (list[str]): The columns of the input data to be used for clustering.
        params (dict[str, str|int|float], optional): A dictionary of parameters for the clustering algorithm. Defaults to None.

    Attributes:
        strategy (ClusterStrategies): The clustering strategy.
        model (Any): The clustering model.
        X (ndarray): The input data for clustering.

    Methods:
        fit(): Fits the cluster model to the input data.
        predict(): Predicts the cluster labels for the input data.
        fit_predict(): Fits the cluster model to the input data and returns the cluster labels.
        get_labels(): Returns the cluster labels.
        get_inertia(): Calculates the within-cluster inertia.
        get_centroids(): Retrieves the cluster centroids.

    Raises:
        ValueError: If the strategy is not specified.
        NotFittedError: If the model hasn't been fitted yet.
    """

    _CLUSTERS: dict[ClusterStrategies, Any] = {
        ClusterStrategies.DBSCAN: DBSCAN,
        ClusterStrategies.KMeans: KMeans,
    }

    def __init__(
        self,
        strategy: ClusterStrategies,
        data: DataFrame,
        cols: list[str],
        *,
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
        self.X = data[cols].to_numpy()

    def fit(self) -> "Cluster":
        """
        Fits the cluster model to the input data `X`.

        Args:
            X: The input data to be used for training.

        Returns:
            Cluster: The `Cluster` object.
        """
        return self.model.fit(self.X)

    def predict(self) -> ndarray:
        """
        Returns:
            ndarray: An array of predicted labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.labels_
        except NotFittedError as e:
            raise e("You have to fit the model first.")

    def fit_predict(self) -> ndarray:
        """
        Fits the cluster model to the input data `X`.

        Args:
            X: The input data to be used for training.

        Returns:
            ndarray: An array of cluster labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        return self.model.fit_predict(self.X)

    def get_labels(self) -> ndarray:
        """
        Returns:
            ndarray: An array of cluster labels.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.labels_
        except NotFittedError as e:
            raise e("You have to fit the model first.")

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
            except NotFittedError as e:
                raise e("You have to fit the model first.")
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
            except NotFittedError as e:
                raise e("You have to fit the model first.")
        else:
            raise ValueError("This model does not support get_centroids.")
