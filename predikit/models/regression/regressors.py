from ._base import(
    BaseRegressor,
    RegressorStrategies
)

from typing import Any
from ..._typing import DataFrame, Series
from numpy import ndarray

from sklearn.ensemble import(
    RandomForestRegressor,
    AdaBoostRegressor
)

from lightgbm import LGBMRegressor
from sklearn.svm import SVR
from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

class Regressors(BaseRegressor):
    _REGRESSORS: dict[RegressorStrategies, Any] = {
        RegressorStrategies.SVR: SVR,
        RegressorStrategies.CatBoostRegressor: CatBoostRegressor,
        RegressorStrategies.LinearRegression: LinearRegression,
        RegressorStrategies.LGBMRegressor: LGBMRegressor,
        RegressorStrategies.RandomForestRegressor: RandomForestRegressor,
        RegressorStrategies.XGBRegressor: XGBRegressor,
        RegressorStrategies.AdaBoostRegressor: AdaBoostRegressor,
        RegressorStrategies.KNeighborsRegressor: KNeighborsRegressor,
        RegressorStrategies.DecisionTreeRegressor: DecisionTreeRegressor,
    }

    def __init__(self, strategy: RegressorStrategies, **regressor_params) -> None:
        self.strategy = RegressorStrategies.from_str(strategy)
        self.model = self._REGRESSORS[self.strategy](**regressor_params)

    def fit(self, X:DataFrame, Y:Series) -> Any:
        self.model.fit(X, Y)

    def score(self, X:DataFrame, Y:Series) -> float:
        return self.model.score(X, Y)

    def predict(self, X: DataFrame) -> ndarray:
        return self.model.predict(X)