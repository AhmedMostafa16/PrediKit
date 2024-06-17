from typing import Tuple

import h2o
from h2o.automl import H2OAutoML
import h2o.display
import numpy as np
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
    params: dict[str, str | int | float | bool] = None
):
    h2o.init() if params is None else h2o.init(**params)


def import_file(path: str) -> h2o.H2OFrame:
    return h2o.import_file(path)


def split_train_test(
    data: h2o.H2OFrame, ratios: list[int] = [0.8], seed: int = None
) -> Tuple[h2o.H2OFrame, h2o.H2OFrame]:
    train, test = data.split_frame(ratios=ratios, seed=seed)
    return (train, test)


class AutoML:
    def __init__(
        self,
        model_type: str = None,
        max_runtime_secs: int = None,
        max_models: int = None,
        balance_classes: bool = False,
        class_sampling_factors: list[float] = None,
        stopping_metric: str = "AUTO",
        nfolds: int = -1,
        include_algos: list[str] = None,
        exclude_algos: list[str] = None,
        seed: int = None,
    ) -> None:
        self.model_type = model_type
        self.model = H2OAutoML(
            max_runtime_secs=max_runtime_secs,
            max_models=max_models,
            balance_classes=balance_classes,
            class_sampling_factors=class_sampling_factors,
            stopping_metric=stopping_metric,
            nfolds=nfolds,
            include_algos=include_algos,
            exclude_algos=exclude_algos,
            seed=seed,
        )
        self.best_model = None
        h2o.display.toggle_user_tips(False)
        self.train_cols_length = None
        self.target = None
        self.train_frame = None
        self.test_frame = None

    def train(
        self,
        x: list[str] = None,
        y: str = None,
        training_frame: h2o.H2OFrame = None,
        validation_frame: h2o.H2OFrame = None,
    ):
        # changes all columns with less than or equal to 2 unique values to factor (categorical).
        factor_cols = []
        for col in training_frame.columns:
            if len(training_frame[col].unique()) <= 2:
                training_frame[col] = training_frame[col].asfactor()
                factor_cols.append(col)

        # changes all columns with less than or equal to 2 unique values to factor (categorical) if validation_frame was provided.
        if validation_frame and factor_cols:
            for col in factor_cols:
                # if len(validation_frame[col].unique()) <= 2:
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
        predictions_train = self.model.predict(self.train_frame)
        predictions_test = self.model.predict(self.test_frame)
        if self.model_type == "classifier":
            with h2o.utils.threading.local_context(
                polars_enabled=True, datatable_enabled=True
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
            feedback = self.classification_feedback(
                test_frame, pred_test_frame, train_frame, pred_train_frame
            )
        else:
            with h2o.utils.threading.local_context(
                polars_enabled=True, datatable_enabled=True
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
            feedback = self.regression_feedback(
                test_frame,
                pred_test_frame,
                train_frame,
                pred_train_frame,
                self.train_cols_length,
            )
        return feedback

    def get_best_model(self):
        return self.best_model

    def model_performance(
        self,
        test_data: h2o.H2OFrame,
    ):
        return self.best_model.model_performance(test_data=test_data)

    def confusion_matrix(self):
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
        return self.model.explain(data)

    def learning_curve_plot(self):
        return self.best_model.learning_curve_plot()

    def varimp_heatmap(self):
        return h2o.varimp_heatmap(self.model)

    def model_correlation_heatmap(self, data: h2o.H2OFrame):
        return h2o.model_correlation_heatmap(self.model, data)

    # saves the model as MOJO.
    def save_mojo(self, path: str, force: bool = False):
        self.best_model.save_mojo(path, force)

    # saves the model as file.
    @classmethod
    def save_model(cls, model, path: str, force: bool = False):
        h2o.save_model(model=model, path=path, force=force)

    def classification_feedback(
        self,
        y_true_test: np.array,
        y_pred_test: np.array,
        y_true_train: np.array,
        y_pred_train: np.array,
    ) -> str:
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
            feedback += f"Good model accuracy (Accuracy: {(acc_test_score * 100):.3f}%)\n"
        elif acc_test_score >= 0.7:
            feedback += f"Moderate model accuracy (Accuracy: {(acc_test_score * 100):.3f}%)\n"
        else:
            feedback += f"Low model accuracy. this indicates insufficient training data or model complexity (Accuracy: {(acc_test_score * 100):.3f}%)\n"
        if auc_roc_score >= 0.9:
            feedback += f"Excellent AUC_ROC score (AUC_ROC: {(auc_roc_score * 100):.3f}%)\n"
        elif auc_roc_score >= 0.7:
            feedback += (
                f"Good AUC_ROC score (AUC_ROC: {(auc_roc_score * 100):.3f}%)\n"
            )
        else:
            feedback += f"Poor AUC_ROC score. Poor AUC_ROC may indicate need for more data or model tuning (AUC_ROC: {(auc_roc_score * 100):.3f}%)\n"
        if pr_score >= 0.75:
            feedback += (
                f"High model precision (Precision: {(pr_score * 100):.3f}%)\n"
            )
        elif pr_score >= 0.5:
            feedback += f"Moderate model precision (Precision: {(pr_score * 100):.3f}%)\n"
        else:
            feedback += f"Low model precision. Low precision suggests class imbalance (Precision: {(pr_score * 100):.3f}%)\n"
        if recall_score >= 0.75:
            feedback += (
                f"High model recall (Recall: {(recall_score * 100):.3f}%)\n"
            )
        elif recall_score >= 0.5:
            feedback += f"Moderate model recall (Recall: {(recall_score * 100):.3f}%)\n"
        else:
            feedback += f"Low model recall. Low recall can indicate a need for more training data (Recall: {(recall_score * 100):.3f}%)\n"
        if f1score >= 0.75:
            feedback += (
                f"High model F1 Score (F1 Score: {(f1score * 100):.3f}%)\n"
            )
        elif f1score >= 0.5:
            feedback += (
                f"Moderate model F1 Score (F1 Score: {(f1score * 100):.3f}%)\n"
            )
        else:
            feedback += f"Low model F1 Score. Low F1 Score can indicate class imbalance or insufficient training (F1Score: {(f1score * 100):.3f}%)\n"
        if len(np.unique(y_true_test)) <= 2:
            if logloss_score < 0.5:
                feedback += (
                    f"Good model Log Loss (LogLoss: {(logloss_score):.3f}%)\n"
                )
            else:
                feedback += f"Poor model Log Loss. High log loss can indicate a need for more data or model tuning. Lower Log Loss is better (LogLoss: {(logloss_score):.3f})\n"
        if train_vs_test_accuracy <= 0.05:
            feedback += f"The model is not overfitting the data. (Train vs Test accuracy: {(train_vs_test_accuracy * 100):.3f}%)\n"
        else:
            feedback += f"The model is overfitting the data. Large differences can indicate overfitting (Train vs Test accuracy: {(train_vs_test_accuracy * 100):.3f}%)\n"

        return feedback

    def regression_feedback(
        self,
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
            feedback += f"Good R2 score (R2 score: {(r2_test * 100):.3f}%)\n"
        elif r2_test >= 0.5:
            feedback += (
                f"Moderate R2 score (R2 score: {(r2_test * 100):.3f}%)\n"
            )
        else:
            feedback += f"Poor R2 score. Low R2 score can indicate model underfitting or insufficient data. (R2 score: {(r2_test * 100):.3f}%)\n"
        if adjusted_r2 >= 0.8:
            feedback += f"Good Adjusted R2 score (Adjusted R2 score: {(adjusted_r2 * 100):.3f}%)\n"
        elif adjusted_r2 >= 0.5:
            feedback += f"Moderate Adjusted R2 score (Adjusted R2 score: {(adjusted_r2 * 100):.3f}%)\n"
        else:
            feedback += f"Poor Adjusted R2 score. Low Adjusted R2 score can indicate model underfitting or insufficient data. (Adjusted R2 score: {(adjusted_r2 * 100):.3f}%)\n"
        if mape <= 0.1:
            feedback += f"Good MAPE score (MAPE: {(mape * 100):.3f}%)\n"
        elif mape <= 0.2:
            feedback += f"Moderate MAPE score (MAPE: {(mape * 100):.3f}%)\n"
        else:
            feedback += f"Poor MAPE score. High MAPE indicates a need for more training or data quality issues. (MAPE: {(mape * 100):.3f}%)\n"
        if train_vs_test_r2_score <= 0.1:
            feedback += f"The model is not overfitting the data. (Train vs Test R2 score: {(train_vs_test_r2_score * 100):.3f}%)\n"
        else:
            feedback += f"The model is overfitting the data. Large differences can indicate overfitting (Train vs Test R2 score: {(train_vs_test_r2_score * 100):.3f}%)\n"
        feedback += f"MAE: {mae}\nMSE: {mse}\nRMSE: {rmse_test}"

        return feedback
