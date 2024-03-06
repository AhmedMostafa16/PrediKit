from ._base import(
    BaseCluster,
    ClusterStrategies
)
from typing import Any
from ..._typing import DataFrame, Series
from sklearn.cluster import DBSCAN, KMeans

class Clusters(BaseCluster):
    _CLUSTERS: dict[ClusterStrategies, Any] = {
        ClusterStrategies.DBSCAN: DBSCAN,
        ClusterStrategies.KMeans: KMeans
    }

    def __init__(self, strategy: ClusterStrategies, **cluster_params) -> None:
        self.strategy = ClusterStrategies.from_str(strategy)
        self.model = self._CLUSTERS[self.strategy](**cluster_params)

    def fit_predict(self, X:DataFrame) -> Any:
        return self.model.fit_predict(X)
