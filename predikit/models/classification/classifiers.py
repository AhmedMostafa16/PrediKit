from ._base import(
    ClassifierStrategies,
    BaseClassifier
)
from ..._typing import DataFrame, Series
from numpy import ndarray, log

from typing import Any
from sklearn.ensemble import(
    RandomForestClassifier,
    AdaBoostClassifier
)

from lightgbm import LGBMClassifier
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression


class Classifiers(BaseClassifier):
    _CLASSIFIERS: dict[ClassifierStrategies, Any] = {
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

    def __init__(self, strategy: ClassifierStrategies, **classifier_params) -> None:
        self.strategy = ClassifierStrategies.from_str(strategy)
        self.model = self._CLASSIFIERS[self.strategy](**classifier_params)

    def fit(self, X:DataFrame, Y:Series) -> Any:
        self.model.fit(X, Y)

    def score(self, X:DataFrame, Y:Series) -> float:
        return self.model.score(X, Y)

    def predict(self, X: DataFrame) -> ndarray:
        return self.model.predict(X)

    def predict_proba(self, X:DataFrame) -> ndarray:
        return self.model.predict_proba(X)

    def predict_log_proba(self, X: DataFrame) -> ndarray:
        return log(self.predict_proba(X))
