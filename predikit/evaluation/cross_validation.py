import joblib
from pandas import DataFrame
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import GridSearchCV


class CrossValidation:
    """
    A class to perform cross-validation on a given model.

    ...

    Attributes
    ----------
    model : Model_type
        The model to be used for cross-validation.
    X : array-like of shape (n_samples, n_features)
        Training data.
    y : array-like of shape (n_samples,)
        Target values.
    cv : int, default=5
        Number of folds for cross-validation.
    folds : iterable
        Generator of train/test indices for each fold.
    scores : list
        List of scores for each fold.

    Methods
    -------
    _get_folds():
        Returns a generator of train/test indices for each fold.
    _get_scores():
        Returns a list of scores for each fold.
    get_mean_score():
        Returns the mean of the scores.
    get_std_score():
        Returns the standard deviation of the scores.
    get_scores():
        Returns the list of scores for each fold.
    get_model():
        Returns the model used for cross-validation.
    """

    _GRIDS = dict[str, dict[str, list[str | int | float]]] = {
        "LogisticRegression": {
            "penalty": ["l1", "l2"],
            "C": [0.1, 1, 10],
            "solver": ["liblinear", "saga"],
            "max_iter": [100, 300, 500, 1000],
        },
        "KNeighborsClassifier": {
            "n_neighbors": [3, 5, 7, 9],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan", "minkowski"],
        },
        "SVC": {
            "C": [0.1, 1, 10, 100],
            "kernel": ["linear", "rbf", "poly", "sigmoid"],
            "gamma": ["scale", "auto"],
        },
        "DecisionTreeClassifier": {
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "criterion": ["gini", "entropy"],
        },
        "XGBClassifier": {
            "n_estimators": [100, 200, 500],
            "max_depth": [3, 6, 10],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.6, 0.8, 1.0],
            "colsample_bytree": [0.6, 0.8, 1.0],
        },
        "AdaBoostClassifier": {
            "n_estimators": [50, 100, 200],
            "learning_rate": [0.01, 0.1, 1.0],
            "algorithm": ["SAMME", "SAMME.R"],
        },
        "RandomForestClassifier": {
            "n_estimators": [100, 200, 300],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        },
        "LGBMClassifier": {
            "num_leaves": [31, 50, 100],
            "max_depth": [-1, 10, 20],
            "learning_rate": [0.01, 0.05, 0.1],
            "n_estimators": [100, 200, 500],
            "min_child_samples": [20, 30, 40],
            "subsample": [0.6, 0.8, 1.0],
        },
        "CatBoostClassifier": {
            "iterations": [100, 500, 1000],
            "depth": [6, 8, 10],
            "learning_rate": [0.01, 0.05, 0.1],
            "l2_leaf_reg": [3, 5, 7],
        },
        "LinearRegression": {"fit_intercept": [True]},
        "KNeighborsRegressor": {
            "n_neighbors": [3, 5, 7, 9],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan", "minkowski"],
        },
        "SVR": {
            "C": [0.1, 1, 10, 100],
            "kernel": ["linear", "rbf", "poly", "sigmoid"],
            "gamma": ["scale", "auto"],
        },
        "DecisionTreeRegressor": {
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "criterion": [
                "squared_error",
                "friedman_mse",
                "absolute_error",
                "poisson",
            ],
        },
        "XGBRegressor": {
            "n_estimators": [100, 200, 500],
            "max_depth": [3, 6, 10],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.6, 0.8, 1.0],
            "colsample_bytree": [0.6, 0.8, 1.0],
        },
        "AdaBoostRegressor": {
            "n_estimators": [50, 100, 200],
            "learning_rate": [0.01, 0.1, 1.0],
            "loss": ["linear", "square", "exponential"],
        },
        "RandomForestRegressor": {
            "n_estimators": [100, 200, 300],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        },
        "LGBMRegressor": {
            "num_leaves": [31, 50, 100],
            "max_depth": [-1, 10, 20],
            "learning_rate": [0.01, 0.05, 0.1],
            "n_estimators": [100, 200, 500],
            "min_child_samples": [20, 30, 40],
            "subsample": [0.6, 0.8, 1.0],
        },
        "CatBoostRegressor": {
            "iterations": [100, 500, 1000],
            "depth": [6, 8, 10],
            "learning_rate": [0.01, 0.05, 0.1],
            "l2_leaf_reg": [3, 5, 7],
        },
    }

    def __init__(
        self, model, data: DataFrame, target: str, cv: int = 5
    ) -> None:
        """
        Constructs all the necessary attributes for the cross_validation object.

        Parameters
        ----------
            model : Model_type
                The model to be used for cross-validation.
            X : array-like of shape (n_samples, n_features)
                Training data.
            y : array-like of shape (n_samples,)
                Target values.
            cv : int, default=5
                Number of folds for cross-validation.
        """
        self.grid = GridSearchCV(
            model,
            param_grid=self._GRIDS[model.__class__.__name__],
            cv=cv,
            n_jobs=-1,
        )
        self.X, self.y = data.drop(target, axis=1), data[target]

    def fit(self, *args):
        self.grid.fit(self.X, self.y)

    def get_best_params(self) -> dict[str, str | int | float]:
        try:
            return self.grid.best_params_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def get_best_score(self) -> float:
        try:
            return self.grid.best_score_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def get_best_estimator(self):
        try:
            return self.grid.best_estimator_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def save_model(self, path: str):
        try:
            joblib.dump(self.grid.best_estimator_, path)
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")
