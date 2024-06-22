from sklearn.model_selection import KFold, learning_curve
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
    roc_curve,
    auc,
    plot_confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
)
import matplotlib.pyplot as plt
import numpy as np
from predikit.models import Model_type


class Metrics:
    """
    Class for calculating evaluation metrics between ground truth and predicted values.

    Parameters
    ----------
    metric : str
        The metric to be calculated. Options: "accuracy", "precision", "recall", "f1".
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated targets as returned by a classifier.
    """

    def __init__(self, metric, y_true, y_pred):
        """
        Constructs all the necessary attributes for the Metrics object.

        Parameters
        ----------
        metric : str
            The metric to be calculated. Options: "accuracy", "precision", "recall", "f1".
        y_true : array-like of shape (n_samples,)
            Ground truth (correct) target values.
        y_pred : array-like of shape (n_samples,)
            Estimated targets as returned by a classifier.
        """
        self.metric = metric
        self.y_true = y_true
        self.y_pred = y_pred

    _metrics = {
        "accuracy": accuracy_score,
        "precision": precision_score,
        "recall": recall_score,
        "f1": f1_score,
    }

    def metric(self):
        """Returns the specified metric score between y_true and y_pred"""
        return self._metrics[self.metric](self.y_true, self.y_pred)

    def plot_confusion_matrix_func(self, X_test, y_test):
        """
        Plots the confusion matrix.

        Parameters
        ----------
        X_test : array-like of shape (n_samples, n_features)
            Test data.
        y_test : array-like of shape (n_samples,)
            True labels for X_test.
        """
        plot_confusion_matrix(self.model, X_test, y_test)
        plt.title("Confusion Matrix")
        plt.show()

    def plot_roc_auc(self, X_test, y_test):
        """
        Plots the ROC curve and AUC.

        Parameters
        ----------
        X_test : array-like of shape (n_samples, n_features)
            Test data.
        y_test : array-like of shape (n_samples,)
            True labels for X_test.
        """
        y_score = self.model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_score)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, label="ROC curve (area = %0.2f)" % roc_auc)

    def get_mse(self):
        """Returns the mean squared error between y_true and y_pred"""
        return mean_squared_error(self.y_true, self.y_pred)

    def get_mae(self):
        """Returns the mean absolute error between y_true and y_pred"""
        return mean_absolute_error(self.y_true, self.y_pred)

    def get_rmse(self):
        """Returns the root mean squared error between y_true and y_pred"""
        return root_mean_squared_error(self.y_true, self.y_pred)
