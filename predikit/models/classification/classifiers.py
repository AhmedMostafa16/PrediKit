
from ._base import(
    ClassifierStrategies,
    BaseClassifier
)
from ..._typing import DataFrame, Series

from typing import Any
from sklearn.ensemble import(
    RandomForestClassifier
)

from lightgbm import LGBMClassifier

class Classifiers(BaseClassifier):
    _CLASSIFIERS: dict[ClassifierStrategies, Any] = {
        ClassifierStrategies.RandomForestClassifier: RandomForestClassifier,
        ClassifierStrategies.LGBMClassifier: LGBMClassifier,
    }

    def __init__(self, strategy: ClassifierStrategies, **classifier_params):
        self.model = self._CLASSIFIERS[strategy](**classifier_params)

    def fit(self, X:DataFrame, Y:Series):
        self.model.fit(X, Y)

    def score(self, X:DataFrame, Y:Series):
        return self.model.score(X, Y)

    def predict(self, X: DataFrame):
        return self.model.predict(X)

    def predict_proba(self, X:DataFrame):
        return self.mode.predic_proba(X)

    def predict_log_proba(self, X: DataFrame):
        return self.model.predict_log_proba(X)
