import h2o
from h2o.automl import H2OAutoML
from typing import Tuple


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

    def train(
        self,
        x: list[str] = None,
        y: str = None,
        training_frame: h2o.H2OFrame = None,
        validation_frame: h2o.H2OFrame = None,
    ):
        self.model.train(
            x=x,
            y=y,
            training_frame=training_frame,
            validation_frame=validation_frame,
        )
        self.best_model = self.model.leader
        return self.best_model

    def get_best_model(self):
        return self.best_model

    def model_performance(
        self,
        test_data: h2o.H2OFrame,
    ):
        return self.best_model.model_performance(test_data=test_data)

    def confusion_matrix(self, threshold: int = None):
        return self.best_model.confusion_matrix(thresholds=threshold)

    def explain(self, data: h2o.H2OFrame):
        return self.model.explain(data)

    def learning_curve_plot(self):
        return self.best_model.learning_curve_plot()

    def varimp_heatmap(self):
        return h2o.varimp_heatmap(self.model)

    def model_correlation_heatmap(self, data: h2o.H2OFrame):
        return h2o.model_correlation_heatmap(self.model, data)

    def save_model(model, path: str, force: bool = False):
        h2o.save_model(model=model, path=path, force=force)
