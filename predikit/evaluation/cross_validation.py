import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import LearningCurveDisplay
from sklearn.model_selection import (
    KFold,
    learning_curve,
)

from predikit.models import Model_type


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
    n_folds : int, default=5
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

    def __init__(self, model: Model_type, X, y, n_folds=5):
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
            n_folds : int, default=5
                Number of folds for cross-validation.
        """
        self.model = model
        self.X = X
        self.y = y
        self.n_folds = n_folds
        self.folds = self._get_folds()
        self.scores = self._get_scores()

    def _get_folds(self):
        """Returns a generator of train/test indices for each fold"""
        return KFold(n_splits=self.n_folds).split(self.X)

    def _get_scores(self):
        """
        Returns a list of scores for each fold.

        The model is fitted and scored on each fold.
        """
        scores = []
        for train_index, test_index in self.folds:
            X_train, X_test = self.X[train_index], self.X[test_index]
            y_train, y_test = self.y[train_index], self.y[test_index]
            self.model.fit(X_train, y_train)
            scores.append(self.model.score(X_test, y_test))
        return scores

    def get_mean_score(self):
        """Returns the mean of the scores"""
        return np.mean(self.scores)

    def get_std_score(self):
        """Returns the standard deviation of the scores"""
        return np.std(self.scores)

    def get_scores(self):
        """Returns the list of scores for each fold"""
        return self.scores

    def get_model(self):
        """Returns the model used for cross-validation"""
        return self.model

    def plot_learning_curve(self, train_sizes=[50, 80, 110], cv=None):
        """

        Plots the learning curve for the model using the provided training sizes and cross-validation strategy.

        Parameters
        ----------
        train_sizes : array-like, default=[50, 80, 110]
        The number of training examples that will be used to generate the learning curve.
        cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy. If None, the class's n_folds attribute is used.

        """

        if cv is None:
            cv = self.n_folds

        train_sizes, train_scores, test_scores = learning_curve(
            self.model,
            self.X,
            self.y,
            train_sizes=train_sizes,
            cv=cv,
            n_jobs=-1,
        )

        fig, ax = plt.subplots()
        LearningCurveDisplay.from_estimator(
            self.model, self.X, self.y, ax=ax, train_sizes=train_sizes, cv=cv
        )
        plt.show()
