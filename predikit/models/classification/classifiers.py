from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from numpy import (
    log,
    ndarray,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
)
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from ..._typing import MatrixLike
from ._base import (
    BaseClassifier,
    ClassifierStrategies,
)
import joblib

class Classifier(BaseClassifier):
    """
    A class that unifies various classification algorithms for efficient model training and prediction.

    ### Parameters
    strategy : {"RandomForestClassifier", "LGBMClassifier",
    "SVC", "CatBoostClassifier", "KNeighborsClassifier",
    "DecisionTreeClassifier", "XGBClassifier", "LogisticRegression",
    "AdaBoostClassifier"}, default= None

    params: a dictionary of parameters {'parameter': value -> (str, int or float)}.
    """

    _CLASSIFIERS: dict = {
        ClassifierStrategies.RandomForestClassifier: RandomForestClassifier,
        ClassifierStrategies.LGBMClassifier: LGBMClassifier,
        ClassifierStrategies.SVC: SVC,
        ClassifierStrategies.CatBoostClassifier: CatBoostClassifier,
        ClassifierStrategies.KNeighborsClassifier: KNeighborsClassifier,
        ClassifierStrategies.DecisionTreeClassifier: DecisionTreeClassifier,
        ClassifierStrategies.XGBClassifier: XGBClassifier,
        ClassifierStrategies.LogisticRegression: LogisticRegression,
        ClassifierStrategies.AdaBoostClassifier: AdaBoostClassifier,
    }

    def __init__(
        self,
        strategy: ClassifierStrategies | None = None,
        params: dict[str, str | int | float] = None,
    ) -> None:
        if params is None:
            params = {}
        if strategy is None:
            raise ValueError("Select a classifier.")
        else:
            self.strategy = ClassifierStrategies.from_str(strategy)

        if params is None:
            self.model = self._CLASSIFIERS[self.strategy]()
        else:
            self.model = self._CLASSIFIERS[self.strategy](**params)

    def fit(self, X: MatrixLike, y: MatrixLike) -> "Classifier":
        """
        Fits the classifier model to the input data `X` and target labels `y`.

        Args:
            X (MatrixLike): The input data to be used for training.
            y (MatrixLike): The target labels for the training data.

        Returns:
            Classifier: The `Classifier` object.
        """
        if (
            self.strategy is ClassifierStrategies.XGBClassifier
            and y.dtype
            in [
                "object",
                "string",
            ]
        ):
            y = LabelEncoder().fit_transform(y)
        return self.model.fit(X, y)

    def score(self, X: MatrixLike, y: MatrixLike) -> float:
        """
        Evaluates the model's performance on the given data and labels.

        Args:
            X: The input data to be evaluated.
            y: The true labels for the input data.

        Returns:
            float: A score representing the model's performance (e.g., accuracy).

        Raises:
            NotFittedError: If the model hasn't been fitted yet.
        """
        try:
            if (
                self.strategy is ClassifierStrategies.XGBClassifier
                and y.dtype
                in [
                    "object",
                    "string",
                ]
            ):
                y = LabelEncoder().fit_transform(y)
            return self.model.score(X, y)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict(self, X: MatrixLike) -> ndarray:
        """
        Predicts class labels for unseen data.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return self.model.predict(X)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict_proba(self, X: MatrixLike) -> ndarray:
        """
        Predicts class probabilities for each data point.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return self.model.predict_proba(X)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict_log_proba(self, X: MatrixLike) -> ndarray:
        """
        Predicts the logarithm of class probabilities for each data point.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return log(self.predict_proba(X))
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def get_model(self) -> "Classifier":
        """
        Returns the classifier model object.

        Returns:
            Classifier: The classifier model object.
        """
        try:
            return self.model
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def save_model(self, path: str) -> None:
        """
        Saves the model to a file.

        Args:
            path (str): The path to save the model to.
        """
        try:
            joblib.dump(self.model, path)
        except Exception:
            raise NotFittedError("You have to fit the model first.")
