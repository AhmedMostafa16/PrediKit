from ._base import(
    ClassifierStrategies,
    BaseClassifier
)
from ..._typing import MatrixLike, Any
from numpy import ndarray, log
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import LabelEncoder

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


class Classifier(BaseClassifier):
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

    def __init__(self, strategy: ClassifierStrategies = None,
                params: dict[str, str | int | float ] = None) -> None:
        if strategy is None:
            raise ValueError('Select a classifier.')
        else:
            self.strategy = ClassifierStrategies.from_str(strategy)

        if params is None:
            self.model = self._CLASSIFIERS[self.strategy]()
        else:
            self.model = self._CLASSIFIERS[self.strategy](**params)

    def fit(self, X: MatrixLike, y: MatrixLike) -> "Classifier":
        if self.strategy is ClassifierStrategies.XGBClassifier and y.dtype in ['object', 'string']:
            y = LabelEncoder().fit_transform(y)
        return self.model.fit(X, y)

    def score(self, X: MatrixLike, y: MatrixLike) -> float:
        try:
            if self.strategy is ClassifierStrategies.XGBClassifier and y.dtype in ['object', 'string']:
                y = LabelEncoder().fit_transform(y)
            return self.model.score(X, y)
        except:
            raise NotFittedError('You have to fit the model first.')

    def predict(self, X: MatrixLike) -> ndarray:
        try: 
            return self.model.predict(X)
        except:
            raise NotFittedError('You have to fit the model first.')

    def predict_proba(self, X:MatrixLike) -> ndarray:
        try:
            return self.model.predict_proba(X)
        except:
            raise NotFittedError('You have to fit the model first.')

    def predict_log_proba(self, X: MatrixLike) -> ndarray:
        try:
            return log(self.predict_proba(X))
        except:
            raise NotFittedError('You have to fit the model first.')