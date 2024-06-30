from typing import Tuple

import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    auc,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


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

    def __init__(self, y_true, y_pred, y_pred_proba):
        """
        Initialize the Metrics object.

        Parameters:
        - y_true: The true labels.
        - y_pred: The predicted labels.
        - y_pred_proba: The predicted probabilities for each class.
        """
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_pred_proba = y_pred_proba

    def get_confusion_matrix(self):
        """
        Get the confusion matrix.

        Returns:
        - array-like of shape (n_classes, n_classes): The confusion matrix.
        """
        return confusion_matrix(self.y_true, self.y_pred)

    def plot_confusion_matrix(self, labels=None):
        """
        Plots the confusion matrix.

        Parameters
        ----------
        labels : array-like of shape (n_classes,), optional
            List of labels to be displayed on the plot. If not provided, the class labels will be used.

        Returns
        -------
        None
        """
        return ConfusionMatrixDisplay(
            confusion_matrix(self.y_true, self.y_pred), display_labels=labels
        ).plot()

    def get_roc_curve_data(self) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Calculate the Receiver Operating Characteristic (ROC) curve data.

        Returns:
            A tuple containing the false positive rate (fpr), true positive rate (tpr)
            and the area under the ROC curve (roc_auc).
        """
        fpr, tpr, _ = roc_curve(self.y_true, self.y_pred_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        return fpr, tpr, roc_auc

    def plot_roc_auc(self):
        """
        Plots the ROC curve and AUC.

        Parameters
        ----------
        X_test : array-like of shape (n_samples, n_features)
            Test data.
        y_test : array-like of shape (n_samples,)
            True labels for X_test.
        """
        fpr, tpr, _ = roc_curve(self.y_true, self.y_pred_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        return RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc).plot()

    def get_regression_metrics(self) -> Tuple[float, float, float]:
        """
        Calculate regression evaluation metrics.

        Args:
            y_true (array-like): The true values of the target variable.
            y_pred (array-like): The predicted values of the target variable.

        Returns:
            Tuple[float, float, float]: A tuple containing the mean absolute error (MAE),
            mean squared error (MSE), and root mean squared error (RMSE) metrics.

        """
        mae = mean_absolute_error(self.y_true, self.y_pred)
        mse = mean_squared_error(self.y_true, self.y_pred)
        rmse = np.sqrt(mse)
        return mae, mse, rmse

    def get_classification_metrics(
        self,
    ) -> Tuple[float, float, float, float, float]:
        """
        Calculate classification evaluation metrics.

        Returns:
            Tuple[float, float, float, float, float]: A tuple containing the accuracy, precision, recall,
            F1 score and roc_auc score metrics.

        """
        accuracy = accuracy_score(self.y_true, self.y_pred)
        precision = precision_score(self.y_true, self.y_pred)
        recall = recall_score(self.y_true, self.y_pred)
        f1 = f1_score(self.y_true, self.y_pred)
        roc_auc = roc_auc_score(self.y_true, self.y_pred)
        return accuracy, precision, recall, f1, roc_auc
