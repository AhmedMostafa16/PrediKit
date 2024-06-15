from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from numpy import ndarray
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
)
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from ..._typing import (
    Any,
    MatrixLike,
)
from ._base import (
    BaseRegressor,
    RegressorStrategies,
)


class Regressor(BaseRegressor):
    """
    A class that provides a unified interface for various regression algorithms.

    ### Parameters
    strategy : {"RandomForestRegressor", "LGBMRegressor",
    "SVR", "CatBoostRegressor", "KNeighborsRegressor",
    "DecisionTreeRegressor", "XGBRegressor", "LinearRegression",
    "AdaBoostRegressor"}, default= None

    params: a dictionary of parameters {'parameter': value -> (str, int or float)}.
    """

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

    def __init__(
        self,
        strategy: RegressorStrategies = None,
        params: dict[str, str | int | float] = None,
    ) -> None:
        if strategy is None:
            raise ValueError("Select a Regressor.")
        else:
            self.strategy = RegressorStrategies.from_str(strategy)

        if params is None:
            self.model = self._REGRESSORS[self.strategy]()
        else:
            self.model = self._REGRESSORS[self.strategy](**params)

    def fit(self, X: MatrixLike, y: MatrixLike) -> "Regressor":
        """
        Fits the regression model to the input data `X` and target values `y`.

        Args:
            X: The input data to be used for training.
            y: The target values for the training data.

        Returns:
            Regressor: The `Regressor` object.
        """
        return self.model.fit(X, y)

    def score(self, X: MatrixLike, y: MatrixLike) -> float:
        """
        Evaluates the model's performance on the given data and labels.

        Args:
            X: The input data to be evaluated.
            y: The true values for the input data.

        Returns:
            float: A score representing the model's performance (e.g., mean squared error).

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.score(X, y)
        except:
            raise NotFittedError("You have to fit the model first.")

    def predict(self, X: MatrixLike) -> ndarray:
        """
        Predicts continuous target values for unseen data.

        Args:
            X: The input data for prediction.

        Returns:
            ndarray: An array of predicted continous values.

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            return self.model.predict(X)
        except:
            raise NotFittedError("You have to fit the model first.")
