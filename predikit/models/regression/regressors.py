from catboost import CatBoostRegressor
import joblib
from lightgbm import LGBMRegressor
from numpy import ndarray
from pandas import DataFrame
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
)
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from ..._typing import Any
from ._base import (
    BaseRegressor,
    RegressorStrategies,
)


class Regressor(BaseRegressor):
    """
    A class that provides a unified interface for various regression algorithms.

    Parameters
    ----------
    strategy : str
        The regression algorithm to use. Available options are:
        - "RandomForestRegressor"
        - "LGBMRegressor"
        - "SVR"
        - "CatBoostRegressor"
        - "KNeighborsRegressor"
        - "DecisionTreeRegressor"
        - "XGBRegressor"
        - "LinearRegression"
        - "AdaBoostRegressor"

    data : DataFrame
        The input data for training and prediction.

    target : str
        The target variable to predict.

    params : dict[str, str | int | float], optional
        A dictionary of parameters for the chosen classification algorithm.

    Attributes
    ----------
    model : object
        The regression model object.

    X_train : pandas.DataFrame
        The training input data.

    X_test : pandas.DataFrame
        The testing input data.

    y_train : pandas.Series
        The training target values.

    y_test : pandas.Series
        The testing target values.

    Methods
    -------
    fit()
        Fits the regression model to the input data.

    score()
        Evaluates the model's performance on the given data.

    predict()
        Predicts continuous target values for unseen data.

    get_y_true()
        Returns the true target values for the test data.

    get_model()
        Returns the regressor model object.

    save_model(path)
        Saves the model to a file.
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
        strategy: RegressorStrategies,
        data: DataFrame,
        target: str,
        *,
        params: dict[str, str | int | float] = None,
    ) -> None:
        """
        Initialize the Regressor object.

        Parameters
        ----------
        strategy : RegressorStrategies
            The regression algorithm to use.

        data : pandas.DataFrame
            The input data.

        target : str
            The target variable name.

        params : dict[str, str|int|float], optional
            A dictionary of parameters for the chosen regression algorithm.
        """
        if strategy is None:
            raise ValueError("Select a Regressor.")
        else:
            self.strategy = RegressorStrategies.from_str(strategy)

        if params is None:
            self.model = self._REGRESSORS[self.strategy]()
        else:
            self.model = self._REGRESSORS[self.strategy](**params)
        X, y = data.drop(target, axis=1), data[target]
        self.X_train, self.X_test, self.y_train, self.y_test = (
            train_test_split(X, y, test_size=0.2)
        )

    def fit(self) -> "Regressor":
        """
        Fits the regression model to the input data.

        Returns
        -------
        Regressor
            The `Regressor` object.
        """
        return self.model.fit(self.X_train, self.y_train)

    def score(self) -> float:
        """
        Evaluates the model's performance on the given data.

        Returns
        -------
        float
            A score representing the model's performance (e.g., mean squared error).

        Raises
        ------
        NotFittedError
            If the model hasn't been fitted yet.
        """
        try:
            return self.model.score(self.X_test, self.y_test)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict(self) -> ndarray:
        """
        Predicts continuous target values for unseen data.

        Returns
        -------
        ndarray
            An array of predicted continuous values.

        Raises
        ------
        NotFittedError
            If the model hasn't been fitted yet.
        """
        try:
            return self.model.predict(self.X_test)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def get_y_true(self) -> ndarray:
        """
        Returns the true target values for the test data.

        Returns
        -------
        ndarray
            An array of true target values.
        """
        return self.y_test

    def get_model(self) -> "Regressor":
        """
        Returns the regressor model object.

        Returns
        -------
        Regressor
            The regressor model object.

        Raises
        ------
        NotFittedError
            If the model hasn't been fitted yet.
        """
        try:
            return self.model
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def save_model(self, path: str) -> None:
        """
        Saves the model to a file.

        Parameters
        ----------
        path : str
            The path to save the model to.
        """
        try:
            joblib.dump(self.model, path)
        except Exception:
            raise NotFittedError(
                "You have to fit the model first before saving it to a file."
            )
