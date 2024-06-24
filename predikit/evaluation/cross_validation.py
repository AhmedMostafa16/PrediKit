import joblib
from pandas import DataFrame
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import GridSearchCV


class CrossValidation:
    """
    Performs cross-validation for a given model using a specified number of folds.

    Parameters
    ----------
    model : Model_type
        The model to be used for cross-validation.
    data : DataFrame
        The input data for training the model.
    target : str
        The target variable column name.
    cv : int, default=5
        Number of folds for cross-validation.

    Attributes
    ----------
    grid : GridSearchCV
        The grid search object used for cross-validation.
    X : DataFrame
        The input features for training the model.
    y : Series
        The target variable for training the model.

    Methods
    -------
    fit()
        Fits the cross-validation model.
    get_best_params() -> dict[str, str | int | float]
        Returns the best parameters found during cross-validation.
    get_best_score() -> float
        Returns the best score achieved during cross-validation.
    get_best_estimator()
        Returns the best estimator found during cross-validation.
    save_model(path: str)
        Saves the best estimator to a file.
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

    def fit(self):
        """
        Fits the grid.
        """
        self.grid.fit(self.X, self.y)

    def get_best_params(self) -> dict[str, str | int | float]:
        """
        Returns the best parameters found by the grid search.

        Returns:
            dict[str, str | int | float]: A dictionary containing the best parameters.

        Raises:
            NotFittedError: If the grid has not been fitted yet.
        """
        try:
            return self.grid.best_params_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def get_best_score(self) -> float:
        """
        Returns the best score achieved by the grid search.

        Raises:
            NotFittedError: If the grid has not been fitted yet.

        Returns:
            float: The best score achieved by the grid search.
        """
        try:
            return self.grid.best_score_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def get_best_estimator(self):
        """
        Returns the best estimator found by the grid search.

        Raises:
            NotFittedError: If the grid has not been fitted yet.

        Returns:
            The best estimator found by the grid search.
        """
        try:
            return self.grid.best_estimator_
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")

    def save_model(self, path: str):
        """
        Save the best estimator from the grid search to a file.

        Args:
            path (str): The path to save the model.

        Raises:
            NotFittedError: If the grid search has not been fitted yet.
        """
        try:
            joblib.dump(self.grid.best_estimator_, path)
        except NotFittedError as e:
            raise e("The grid has not been fitted yet.")
