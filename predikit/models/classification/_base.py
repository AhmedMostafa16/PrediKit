from abc import (
    ABC,
    abstractmethod,
)
from enum import StrEnum

from numpy import ndarray
from sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
)

from ..._typing import (
    Any,
    MatrixLike,
)


class BaseClassifier(ClassifierMixin, BaseEstimator, ABC):
    """Base class for all classifiers."""

    @abstractmethod
    def fit(X: MatrixLike, Y: MatrixLike) -> "BaseClassifier":
        pass

    @abstractmethod
    def score(X: MatrixLike, Y: MatrixLike) -> float:
        pass

    @abstractmethod
    def predict(X: MatrixLike) -> ndarray:
        pass

    @abstractmethod
    def predict_proba(X: MatrixLike) -> ndarray:
        pass

    def predict_log_proba(X: MatrixLike) -> ndarray:
        pass


class ClassifierStrategies(StrEnum):

    SVC = "SVC"
    XGBClassifier = "XGBClassifier"
    LGBMClassifier = "LGBMClassifier"
    LogisticRegression = "LogisticRegression"
    CatBoostClassifier = "CatBoostClassifier"
    AdaBoostClassifier = "AdaBoostClassifier"
    KNeighborsClassifier = "KNeighborsClassifier"
    DecisionTreeClassifier = "DecisionTreeClassifier"
    RandomForestClassifier = "RandomForestClassifier"

    @classmethod
    def from_str(cls, strategy: str) -> "ClassifierStrategies":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        ClassifierStrategies
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "supportvectorclassifier" | "svc":
                return cls.SVC
            case "xgbc" | "xgboostclassifier" | "xgbclassifier":
                return cls.XGBClassifier
            case "lightgbmclassifier" | "lightclassifier" | "lgbmclassifier":
                return cls.LGBMClassifier
            case "logisticregression":
                return cls.LogisticRegression
            case "cbclassifier" | "catboostclassifier":
                return cls.CatBoostClassifier
            case "adaboostclassifier" | "adclassifier":
                return cls.AdaBoostClassifier
            case "knnclassifier" | "kneighborsclassifier":
                return cls.KNeighborsClassifier
            case "decisiontreeclassifier" | "dcclassifier":
                return cls.DecisionTreeClassifier
            case (
                "forestclassifier" | "rfclassifier" | "randomforestclassifier"
            ):
                return cls.RandomForestClassifier
            case _:
                raise ValueError(f"Invalid classifier strategy: {strategy}")
