from ._base import(
    BaseCluster,
    ClusterStrategies
)
from numpy import ndarray
from ..._typing import MatrixLike, Any
from sklearn.exceptions import NotFittedError

from sklearn.cluster import DBSCAN, KMeans

class Cluster(BaseCluster):
    _CLUSTERS: dict[ClusterStrategies, Any] = {
        ClusterStrategies.DBSCAN: DBSCAN,
        ClusterStrategies.KMeans: KMeans
    }

    def __init__(self, strategy: ClusterStrategies = None,
                params: dict[str, str | int | float ] = None) -> None:
        if strategy is None:
            raise ValueError('Select a Cluster.')
        else:
            self.strategy = ClusterStrategies.from_str(strategy)

        if params is None:
            self.model = self._CLUSTERS[self.strategy]()
        else:
            self.model = self._CLUSTERS[self.strategy](**params)


    def fit(self, X: MatrixLike) -> "Cluster":
        return self.model.fit(X)

    def fit_predict(self, X: MatrixLike) -> ndarray:
        return self.model.fit_predict(X)

    def get_labels(self) -> ndarray:
        try:
            return self.model.labels_
        except:
            raise NotFittedError('You have to fit the model first.')
        
    def get_inertia(self) -> float:
        if self.model in [ClusterStrategies.KMeans,]:
            try:
                return self.model.labels_
            except:
                raise NotFittedError('You have to fit the model first.')
        else:
            raise ValueError('This model does not support get_inertia.')

    def get_centroids(self) -> ndarray:
        if self.model in [ClusterStrategies.KMeans,]:
            try:
                return self.model.cluster_centers_
            except:
                raise NotFittedError('You have to fit the model first.')
        else:
            raise ValueError('This model does not support get_centroids.')

