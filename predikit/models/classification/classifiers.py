from catboost import CatBoostClassifier
import joblib
from lightgbm import LGBMClassifier
from numpy import (
    log,
    ndarray,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
)
from sklearn.model_selection import train_test_split
from pandas import DataFrame
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from ._base import (
    BaseClassifier,
    ClassifierStrategies,
)


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
        strategy: ClassifierStrategies,
        data: DataFrame,
        target: str,
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
        X, y = data.drop(target, axis=1), data[target]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2
        )

    def fit(self) -> "Classifier":
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
            and self.y_train.dtype
            in [
                "object",
                "string",
            ]
        ):
            self.y_train.dtype = LabelEncoder().fit_transform(self.y_train.dtype)
        return self.model.fit(self.X_train, self.y_train)

    def score(self) -> float:
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
                and self.y_test.dtype
                in [
                    "object",
                    "string",
                ]
            ):
                self.y_test = LabelEncoder().fit_transform(self.y_test)
            return self.model.score(self.X_test, self.y_test)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict(self) -> ndarray:
        """
        Predicts class labels for unseen data.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return self.model.predict(self.X_test)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict_proba(self) -> ndarray:
        """
        Predicts class probabilities for each data point.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return self.model.predict_proba(self.X_test)
        except Exception:
            raise NotFittedError("You have to fit the model first.")

    def predict_log_proba(self) -> ndarray:
        """
        Predicts the logarithm of class probabilities for each data point.

        Args:
            X: The input data for prediction.

        Raises:
            `NotFittedError` if the model hasn't been fitted.
        """
        try:
            return log(self.predict_proba(self.X_test))
        except Exception:
            raise NotFittedError("You have to fit the model first.")
        
    def get_y_true(self) -> ndarray:
        """
        Returns the true labels for the test data.

        Returns:
            ndarray: An array of true labels.
        """
        return self.y_test

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
