from abc import(
    ABC, 
    abstractmethod
)

from enum import StrEnum

from sklearn.base import (
    RegressorMixin,
    BaseEstimator
)
from numpy import ndarray
from ..._typing import MatrixLike

class BaseRegressor(RegressorMixin, BaseEstimator, ABC):
    """Base class for all regressors."""

    @abstractmethod
    def fit(X: MatrixLike, Y: MatrixLike) -> "BaseRegressor":
        pass

    @abstractmethod
    def score(X: MatrixLike, Y: MatrixLike) -> float:
        pass

    @abstractmethod
    def predict(X: MatrixLike) -> ndarray:
        pass

class RegressorStrategies(StrEnum):

    SVR = 'SVR'
    XGBRegressor = 'XGBRegressor'
    LGBMRegressor = 'LGBMRegressor'
    LinearRegression = 'LinearRegression'
    CatBoostRegressor = 'CatBoostRegressor'
    AdaBoostRegressor = 'AdaBoostRegressor'
    KNeighborsRegressor = 'KNeighborsRegressor'
    DecisionTreeRegressor = 'DecisionTreeRegressor'
    RandomForestRegressor = 'RandomForestRegressor'

    @classmethod
    def from_str(cls, strategy: str) -> "RegressorStrategies":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        RegressorStrategies
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "supportvectorregressor" | 'svr':
                return cls.SVR
            case "xgbr" | "xgboostregressor" | "xgbregressor":
                return cls.XGBRegressor
            case "lightgbmregressor" | "lightregressor" | "lgbmregressor":
                return cls.LGBMRegressor
            case "linearregression":
                return cls.LinearRegression
            case "cbregressor" | "catboostregressor":
                return cls.CatBoostRegressor
            case "adaboostregressor" | "adregressor":
                return cls.AdaBoostRegressor
            case "knnregressor" | "kneighborsregressor":
                return cls.KNeighborsRegressor
            case "decisiontreeregressor" | "dcregressor":
                return cls.DecisionTreeRegressor
            case "forestregressor" | "rfregressor" | "randomforestregressor":
                return cls.RandomForestRegressor
            case _:
                raise ValueError(f"Invalid regressor strategy: {strategy}")