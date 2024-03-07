from ._base import(
    BaseRegressor,
    RegressorStrategies
)

from ..._typing import MatrixLike, Any
from numpy import ndarray
from sklearn.exceptions import NotFittedError

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

class Regressor(BaseRegressor):
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

    def __init__(self, strategy: RegressorStrategies = None,
                params: dict[str, str | int | float ] = None) -> None:
        if strategy is None:
            raise ValueError('Select a Regressor.')
        else:
            self.strategy = RegressorStrategies.from_str(strategy)

        if params is None:
            self.model = self._REGRESSORS[self.strategy]()
        else:
            self.model = self._REGRESSORS[self.strategy](**params)

    def fit(self, X: MatrixLike, Y: MatrixLike) -> "Regressor":
        return self.model.fit(X, Y)

    def score(self, X: MatrixLike, Y: MatrixLike) -> float:
        try:
            return self.model.score(X, Y)
        except:
            raise NotFittedError('You have to fit the model first.')

    def predict(self, X: MatrixLike) -> ndarray:
        try: 
            return self.model.predict(X)
        except:
            raise NotFittedError('You have to fit the model first.')