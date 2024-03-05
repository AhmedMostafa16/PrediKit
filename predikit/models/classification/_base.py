from abc import(
    ABC, 
    abstractmethod
)

from enum import StrEnum

from sklearn.base import (
    ClassifierMixin,
    BaseEstimator
)

from ..._typing import DataFrame, Series

class BaseClassifier(ClassifierMixin, BaseEstimator, ABC):

    @abstractmethod
    def fit(X: DataFrame, Y: Series):
        pass

    @abstractmethod
    def score(X: DataFrame, Y: Series):
        pass

    @abstractmethod
    def predict(X: DataFrame):
        pass

    @abstractmethod
    def predict_proba(X: DataFrame):
        pass

    def predict_log_proba(X: DataFrame):
        pass

class ClassifierStrategies(StrEnum):

    SVC = 'SVC'
    XGBClassifier = 'XGBClassifier'
    LGBMClassifier = 'LGBMClassifier'
    LogisticRegression = 'LogisticRegression'
    CatBoostClassifier = 'CatBoostClassifier'
    AdaBoostClassifier = 'AdaBoostClassifier'
    KNeighborsClassifier = 'KNeighborsClassifier'
    DecisionTreeClassifier = 'DecisionTreeClassifier'
    RandomForestClassifier = 'RandomForestClassifier'

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
            case "supportvectorclassifier" | 'svc':
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
            case "forestclassifier" | "rfclassifier" | "randomforestclassifier":
                return cls.RandomForestClassifier
            case _:
                raise ValueError(f"Invalid classifier strategy: {strategy}")