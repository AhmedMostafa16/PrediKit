from typing import Tuple

import h2o
from h2o.automl import H2OAutoML
import h2o.display
import numpy as np
from pandas import DataFrame
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.preprocessing import LabelEncoder
from tensorflow.python.keras.metrics import (
    AUC,
    Accuracy,
    BinaryCrossentropy,
    Precision,
    Recall,
)


def initialize_cluster_server(
    params: dict[str, str | int | float | bool] = None,
) -> None:
    """
    Initializes the H2O cluster server.

    Args:
        params (dict[str, str | int | float | bool], optional): A dictionary of parameters to configure the H2O cluster server. Defaults to None.

    Returns:
        None
    """
    h2o.init() if params is None else h2o.init(**params)


def import_file(path: str) -> h2o.H2OFrame:
    """
    Imports a file into an H2OFrame.

    Args:
        path (str): The path to the file to be imported.

    Returns:
        h2o.H2OFrame: The imported file as an H2OFrame object.
    """
    return h2o.import_file(path)


def split_train_test(
    data: h2o.H2OFrame, ratios: list[int] = None, seed: int = None
) -> Tuple[h2o.H2OFrame, h2o.H2OFrame]:
    """
    Split the given H2OFrame into training and testing datasets.

    Args:
        data (h2o.H2OFrame): The input H2OFrame to be split.
        ratios (list[int], optional): The ratios at which to split the data. Defaults to [0.8].
        seed (int, optional): The seed value for random number generation. Defaults to None.

    Returns:
        Tuple[h2o.H2OFrame, h2o.H2OFrame]: A tuple containing the training and testing datasets.
    """
    if ratios is None:
        ratios = [0.8]
    train, test = data.split_frame(ratios=ratios, seed=seed)
    return (train, test)


class AutoML:
    """
    AutoML class for automated machine learning using H2O AutoML.

    Args:
        model_type (str): The type of model to train. Default is None.
        max_runtime_secs (int): The maximum runtime in seconds for the AutoML process. Default is 3600 (1 Hour).
        max_models (int): The maximum number of models to train. Default is None.
        balance_classes (bool): Whether to balance the class distribution of the target variable. Default is False.
        class_sampling_factors (list[float]): The per-class (in lexicographical order) over/under-sampling ratios for the training data. Default is None.
        stopping_metric (str): The metric to use for early stopping. Default is "AUTO".
            The available options are:

            - ``"AUTO"`` (This defaults to ``"logloss"`` for classification, ``"deviance"`` for regression)
            - ``"deviance"``
            - ``"logloss"``
            - ``"mse"``
            - ``"rmse"``
            - ``"mae"``
            - ``"rmsle"``
            - ``"auc"``
            - ``aucpr``
            - ``"lift_top_group"``
            - ``"misclassification"``
            - ``"mean_per_class_error"``
            - ``"r2"``

        sort_metric: Metric to sort the leaderboard by at the end of an AutoML run.
            For binomial classification, select from the following options:

                - ``"auc"``
                - ``"aucpr"``
                - ``"logloss"``
                - ``"mean_per_class_error"``
                - ``"rmse"``
                - ``"mse"``

            For multinomial classification, select from the following options:

                - ``"mean_per_class_error"``
                - ``"logloss"``
                - ``"rmse"``
                - ``"mse"``

            For regression, select from the following options:

                - ``"deviance"``
                - ``"rmse"``
                - ``"mse"``
                - ``"mae"``
                - ``"rmlse"``

            Defaults to ``"AUTO"`` (This translates to ``"auc"`` for binomial classification, ``"mean_per_class_error"`` for multinomial classification, ``"deviance"`` for regression).
        nfolds (int): The number of folds for cross-validation. Default is -1.
        include_algos (list[str]): The list of algorithms to include in the AutoML process.
            This can't be used in combination with ``exclude_algos`` param.

            The full list of options is:

                - ``"DRF"`` (Random Forest and Extremely-Randomized Trees)
                - ``"GLM"``
                - ``"XGBoost"``
                - ``"GBM"``
                - ``"DeepLearning"``
                - ``"StackedEnsemble"``

            Defaults to ``None``
            Usage example::

                include_algos = ["GLM", "DeepLearning", "DRF"]

        exclude_algos (list[str]): The list of algorithms to exclude from the AutoML process.
            This can't be used in combination with ``include_algos`` param.
            Defaults to ``None``
            Usage example::

                exclude_algos = ["GLM", "DeepLearning", "DRF"]

        seed (int): The random seed for reproducibility. Default is None.
        verbosity: Verbosity of the backend messages printed during training.
            Available options are ``None`` (live log disabled), ``"debug"``, ``"info"``, ``"warn"`` or ``"error"``.
            Defaults to ``"warn"``.

    Attributes:
        model_type (str): The type of model to train.
        model (H2OAutoML): The H2O AutoML model.
        best_model: The best model selected by AutoML.
        train_cols_length: The number of columns in the training data.
        target: The target variable.
        train_frame: The training data frame.
        test_frame: The test data frame.

    Methods:
        train: Trains the AutoML model.
        user_feedback: Provides feedback on the performance of the AutoML model.
        get_best_model: Returns the best model selected by AutoML.
        model_performance: Computes the performance of the best model on test data.
        confusion_matrix: Computes and displays the confusion matrix for the best model.
        explain: Generates an explanation for the best model.
        learning_curve_plot: Generates a learning curve plot for the best model.
        varimp_heatmap: Generates a variable importance heatmap for the best model.
        model_correlation_heatmap: Generates a correlation heatmap for the best model.
        save_mojo: Saves the best model as a MOJO file.
        save_model: Saves a given model as a file.
        classification_feedback: Provides feedback on the classification performance of the best model.

    """

    def __init__(
        self,
        model_type: str,
        max_runtime_secs: int = 3600,
        max_models: int = None,
        balance_classes: bool = False,
        class_sampling_factors: list[float] = None,
        stopping_metric: str = "AUTO",
        sort_metric: str = "AUTO",
        nfolds: int = -1,
        include_algos: list[str] = None,
        exclude_algos: list[str] = None,
        seed: int = None,
        verbosity="warn",
    ) -> None:
        initialize_cluster_server()
        self.model_type = model_type
        self.model = H2OAutoML(
            max_runtime_secs=max_runtime_secs,
            max_models=max_models,
            balance_classes=balance_classes,
            class_sampling_factors=class_sampling_factors,
            stopping_metric=stopping_metric,
            sort_metric=sort_metric,
            nfolds=nfolds,
            include_algos=include_algos,
            exclude_algos=exclude_algos,
            seed=seed,
            verbosity=verbosity,
        )
        self.best_model = None
        h2o.display.toggle_user_tips(False)
        self.train_cols_length = None
        self.target = None
        self.train_frame = None
        self.test_frame = None
        if exclude_algos is None:
            exclude_algos = ["StackedEnsemble"]

    def train(
        self,
        y: str,
        training_frame: DataFrame,
        *,
        x: list[str] = None,
        validation_frame: DataFrame = None,
    ):
        """
        Trains the AutoML model.

        Args:
            x (list[str]): The list of predictor columns. Default is None.
            y (str): The target column. Default is None.
            training_frame (h2o.H2OFrame): The training data frame. Default is None.
            validation_frame (h2o.H2OFrame): The validation data frame. Default is None.

        Returns:
            The best model selected by AutoML.

        """
        training_frame = h2o.H2OFrame(training_frame)
        if validation_frame:
            validation_frame = h2o.H2OFrame(validation_frame)

        factor_cols = []
        # changes all columns with less than or equal to 2 unique values to factor (categorical).
        for col in training_frame.columns:
            if len(training_frame[col].unique()) <= 2:
                training_frame[col] = training_frame[col].asfactor()
                factor_cols.append(col)

        # changes the same columns as training frame to factor (categorical) if validation_frame was provided.
        if validation_frame and factor_cols:
            for col in factor_cols:
                validation_frame[col] = validation_frame[col].asfactor()

        # ensures target column is identified as factor if the model is set to classifier.
        if self.model_type == "classifier":
            training_frame[y] = training_frame[y].asfactor()
            if validation_frame:
                validation_frame[y] = validation_frame[y].asfactor()

        self.train_frame, self.test_frame = training_frame.split_frame([0.8])
        self.model.train(
            x=x,
            y=y,
            training_frame=self.train_frame,
            validation_frame=validation_frame,
        )
        self.best_model = self.model.leader
        self.train_cols_length = len(training_frame.columns) - 1
        self.target = y
        return self.best_model

    def user_feedback(self) -> str:
        """
        Provides feedback on the performance of the AutoML model.

        Returns:
            The feedback string.

        """
        predictions_train = self.model.predict(self.train_frame)
        predictions_test = self.model.predict(self.test_frame)
        if self.model_type == "classifier":
            with h2o.utils.threading.local_context(
                polars_enabled=False, datatable_enabled=False
            ):
                pred_train_frame = LabelEncoder().fit_transform(
                    predictions_train["predict"]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                train_frame = LabelEncoder().fit_transform(
                    self.train_frame[self.target]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                pred_test_frame = LabelEncoder().fit_transform(
                    predictions_test["predict"]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                test_frame = LabelEncoder().fit_transform(
                    self.test_frame[self.target]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
            if len(np.unique(test_frame)) > 2:
                pred_test_frame = (pred_test_frame - pred_test_frame.min()) / (
                    pred_test_frame.max() - pred_test_frame.min()
                )
                test_frame = (test_frame - test_frame.min()) / (
                    test_frame.max() - test_frame.min()
                )
                pred_train_frame = (
                    pred_train_frame - pred_train_frame.min()
                ) / (pred_train_frame.max() - pred_train_frame.min())
                train_frame = (train_frame - train_frame.min()) / (
                    train_frame.max() - train_frame.min()
                )
            feedback = AutoML.classification_feedback(
                test_frame, pred_test_frame, train_frame, pred_train_frame
            )
        else:
            with h2o.utils.threading.local_context(
                polars_enabled=False, datatable_enabled=False
            ):
                pred_train_frame = (
                    predictions_train["predict"]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                train_frame = (
                    self.train_frame[self.target]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                pred_test_frame = (
                    predictions_test["predict"]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
                test_frame = (
                    self.test_frame[self.target]
                    .as_data_frame()
                    .to_numpy()
                    .reshape(
                        -1,
                    )
                )
            feedback = AutoML.regression_feedback(
                test_frame,
                pred_test_frame,
                train_frame,
                pred_train_frame,
                self.train_cols_length,
            )
        return feedback

    def get_best_model(self):
        """
        Returns the best model selected by AutoML.

        Returns:
            The best model.

        """
        return self.best_model

    def model_performance(
        self,
        test_data: h2o.H2OFrame,
    ):
        """
        Computes the performance of the best model on test data.

        Args:
            test_data (h2o.H2OFrame): The test data frame.

        Returns:
            The model performance.

        """
        return self.best_model.model_performance(test_data=test_data)

    def confusion_matrix(self):
        """
        Computes and displays the confusion matrix for the best model.

        Returns:
            The confusion matrix plot.

        """
        predictions_test = self.model.predict(self.test_frame)
        with h2o.utils.threading.local_context(
            polars_enabled=True, datatable_enabled=True
        ):
            pred_test_frame = (
                predictions_test["predict"]
                .as_data_frame()
                .to_numpy()
                .reshape(
                    -1,
                )
            )
            test_frame = (
                self.test_frame[self.target]
                .as_data_frame()
                .to_numpy()
                .reshape(
                    -1,
                )
            )
        return ConfusionMatrixDisplay(
            confusion_matrix(test_frame, pred_test_frame)
        ).plot()

    def explain(self, data: h2o.H2OFrame):
        """
        Generates an explanation for the best model.

        Args:
            data (h2o.H2OFrame): The data frame to explain.

        Returns:
            The explanation.

        """
        return self.model.explain(data)

    def learning_curve_plot(self):
        """
        Generates a learning curve plot for the best model.

        Returns:
            The learning curve plot.

        """
        return self.best_model.learning_curve_plot()

    def varimp_heatmap(self):
        """
        Generates a variable importance heatmap for the best model.

        Returns:
            The variable importance heatmap.

        """
        return h2o.varimp_heatmap(self.model)

    def model_correlation_heatmap(self, data: h2o.H2OFrame):
        """
        Generates a correlation heatmap for the best model.

        Args:
            data (h2o.H2OFrame): The data frame.

        Returns:
            The correlation heatmap.

        """
        return h2o.model_correlation_heatmap(self.model, data)

    def save_mojo(self, path: str, force: bool = False):
        """
        Saves the best model as a MOJO file.

        Args:
            path (str): The path to save the MOJO file.
            force (bool): Whether to overwrite an existing file. Default is False.

        """
        self.best_model.save_mojo(path, force)

    @staticmethod
    def save_model(cls, model, path: str, force: bool = False):
        """
        Saves a given model as a file.

        Args:
            model: The model to save.
            path (str): The path to save the model file.
            force (bool): Whether to overwrite an existing file. Default is False.

        """
        h2o.save_model(model=model, path=path, force=force)

    @staticmethod
    def classification_feedback(
        y_true_test: np.array,
        y_pred_test: np.array,
        y_true_train: np.array,
        y_pred_train: np.array,
    ) -> str:
        """
        Provides feedback on the classification performance of the best model.

        Args:
            y_true_test (np.array): The true labels of the test data.
            y_pred_test (np.array): The predicted labels of the test data.
            y_true_train (np.array): The true labels of the training data.
            y_pred_train (np.array): The predicted labels of the training data.

        Returns:
            The feedback string.

        """
        auc_roc = AUC(curve="ROC")
        acc_test = Accuracy()
        acc_train = Accuracy()
        pr = Precision()
        recall = Recall()
        if len(np.unique(y_true_test)) <= 2:
            logloss = BinaryCrossentropy()
            logloss.update_state(y_true_test, y_pred_test)
            logloss_score = logloss.result()

        auc_roc.update_state(y_true_test, y_pred_test)
        acc_test.update_state(y_true_test, y_pred_test)
        acc_train.update_state(y_true_train, y_pred_train)
        pr.update_state(y_true_test, y_pred_test)
        recall.update_state(y_true_test, y_pred_test)

        f1score = (
            2
            * (pr.result() * recall.result())
            / (pr.result() + recall.result())
        )
        auc_roc_score = auc_roc.result()
        acc_test_score = acc_test.result()
        acc_train_score = acc_train.result()
        pr_score = pr.result()
        recall_score = recall.result()
        train_vs_test_accuracy = abs(acc_train_score - acc_test_score) / (
            acc_train_score
        )

        feedback = ""
        if acc_test_score >= 0.9:
            feedback += f"Accuracy: {(acc_test_score * 100):.3f}% (Good model accuracy)\n"
        elif acc_test_score >= 0.7:
            feedback += f"Accuracy: {(acc_test_score * 100):.3f}% (Moderate model accuracy)\n"
        else:
            feedback += f"Accuracy: {(acc_test_score * 100):.3f}% (Low model accuracy. This indicates insufficient training data or model complexity)\n"
        if auc_roc_score >= 0.9:
            feedback += f"AUC_ROC: {(auc_roc_score * 100):.3f}% (Excellent AUC_ROC score)\n"
        elif auc_roc_score >= 0.7:
            feedback += (
                f"AUC_ROC: {(auc_roc_score * 100):.3f}% (Good AUC_ROC score)\n"
            )
        else:
            feedback += f"AUC_ROC: {(auc_roc_score * 100):.3f}% (Poor AUC_ROC score. Poor AUC_ROC may indicate need for more data or model tuning)\n"
        if pr_score >= 0.75:
            feedback += (
                f"Precision: {(pr_score * 100):.3f}% (High model precision)\n"
            )
        elif pr_score >= 0.5:
            feedback += f"Precision: {(pr_score * 100):.3f}% (Moderate model precision)\n"
        else:
            feedback += f"Precision: {(pr_score * 100):.3f}% (Low model precision. Low precision suggests class imbalance)\n"
        if recall_score >= 0.75:
            feedback += (
                f"Recall: {(recall_score * 100):.3f}% (High model recall)\n"
            )
        elif recall_score >= 0.5:
            feedback += f"Recall: {(recall_score * 100):.3f}% (Moderate model recall)\n"
        else:
            feedback += f"Recall: {(recall_score * 100):.3f}% (Low model recall. Low recall can indicate a need for more training data)\n"
        if f1score >= 0.75:
            feedback += (
                f"F1 Score: {(f1score * 100):.3f}% (High model F1 Score)\n"
            )
        elif f1score >= 0.5:
            feedback += (
                f"F1 Score: {(f1score * 100):.3f}% (Moderate model F1 Score)\n"
            )
        else:
            feedback += f"F1 Score: {(f1score * 100):.3f}% (Low model F1 Score. Low F1 Score can indicate class imbalance or insufficient training)\n"
        if len(np.unique(y_true_test)) <= 2:
            if logloss_score < 0.5:
                feedback += (
                    f"Log Loss: {(logloss_score):.3f}% (Good model Log Loss)\n"
                )
            else:
                feedback += f"Log Loss: {(logloss_score):.3f} (Poor model Log Loss. High log loss can indicate a need for more data or model tuning. Lower Log Loss is better)\n"
        if train_vs_test_accuracy <= 0.05:
            feedback += f"Train vs Test accuracy: {(train_vs_test_accuracy * 100):.3f}% (The model is not overfitting the data)\n"
        else:
            feedback += f"Train vs Test accuracy: {(train_vs_test_accuracy * 100):.3f}% (The model is overfitting the data. Large differences can indicate overfitting)\n"

        return feedback

    @staticmethod
    def regression_feedback(
        y_true_test: np.array,
        y_pred_test: np.array,
        y_true_train: np.array,
        y_pred_train: np.array,
        num_of_training_columns: int,
    ) -> str:
        mae = mean_absolute_error(y_true_test, y_pred_test)
        mape = mean_absolute_percentage_error(y_true_test, y_pred_test)
        mse = mean_squared_error(y_true_test, y_pred_test)
        rmse_test = root_mean_squared_error(y_true_test, y_pred_test)
        r2_train = r2_score(y_true_train, y_pred_train)
        r2_test = r2_score(y_true_test, y_pred_test)
        train_vs_test_r2_score = abs(r2_train - r2_test) / (r2_train)
        adjusted_r2 = 1 - (1 - r2_score(y_true_test, y_pred_test)) * (
            len(y_true_test) - 1
        ) / (len(y_true_test) - (num_of_training_columns) - 1)

        feedback = ""
        if r2_test >= 0.8:
            feedback += f"R2 score: {(r2_test * 100):.3f}% (Good R2 score)\n"
        elif r2_test >= 0.5:
            feedback += (
                f"R2 score: {(r2_test * 100):.3f}% (Moderate R2 score)\n"
            )
        else:
            feedback += f"R2 score: {(r2_test * 100):.3f}% (Poor R2 score. Low R2 score can indicate model underfitting or insufficient data)\n"
        if adjusted_r2 >= 0.8:
            feedback += f"Adjusted R2 score: {(adjusted_r2 * 100):.3f}% (Good Adjusted R2 score)\n"
        elif adjusted_r2 >= 0.5:
            feedback += f"Adjusted R2 score: {(adjusted_r2 * 100):.3f}% (Moderate Adjusted R2 score)\n"
        else:
            feedback += f"Adjusted R2 score: {(adjusted_r2 * 100):.3f}% (Poor Adjusted R2 score. Low Adjusted R2 score can indicate model underfitting or insufficient data)\n"
        if mape <= 0.1:
            feedback += f"MAPE: {(mape * 100):.3f}% (Good MAPE score)\n"
        elif mape <= 0.2:
            feedback += f"MAPE: {(mape * 100):.3f}% (Moderate MAPE score)\n"
        else:
            feedback += f"MAPE: {(mape * 100):.3f}% (Poor MAPE score. High MAPE indicates a need for more training or data quality issues)\n"
        if train_vs_test_r2_score <= 0.1:
            feedback += f"Train vs Test R2 score: {(train_vs_test_r2_score * 100):.3f}% (The model is not overfitting the data)\n"
        else:
            feedback += f"Train vs Test R2 score: {(train_vs_test_r2_score * 100):.3f}% (The model is overfitting the data. Large differences can indicate overfitting)\n"
        feedback += f"MAE: {mae}\nMSE: {mse}\nRMSE: {rmse_test}"

        return feedback
