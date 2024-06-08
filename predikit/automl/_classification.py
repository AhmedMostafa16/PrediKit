from pycaret.classification import *

from typing import Any, Callable, Dict, List, Optional, Union
from .._typing import DATAFRAME_LIKE, TARGET_LIKE, SEQUENCE_LIKE, DataFrame


class AutoClassification:
    def __init__(
        self,
        data: Optional[DATAFRAME_LIKE] = None,
        data_func: Optional[Callable[[], DATAFRAME_LIKE]] = None,
        target: TARGET_LIKE = -1,
        index: Union[bool, int, str, SEQUENCE_LIKE] = True,
        train_size: float = 0.7,
        test_data: Optional[DATAFRAME_LIKE] = None,
        ordinal_features: Optional[Dict[str, list]] = None,
        numeric_features: Optional[List[str]] = None,
        categorical_features: Optional[List[str]] = None,
        date_features: Optional[List[str]] = None,
        text_features: Optional[List[str]] = None,
        ignore_features: Optional[List[str]] = None,
        keep_features: Optional[List[str]] = None,
        preprocess: bool = True,
        create_date_columns: List[str] = None,
        imputation_type: Optional[str] = "simple",
        numeric_imputation: Union[int, float, str] = "mean",
        categorical_imputation: str = "mode",
        iterative_imputation_iters: int = 5,
        numeric_iterative_imputer: Union[str, Any] = "lightgbm",
        categorical_iterative_imputer: Union[str, Any] = "lightgbm",
        text_features_method: str = "tf-idf",
        max_encoding_ohe: int = 25,
        encoding_method: Optional[Any] = None,
        rare_to_value: Optional[float] = None,
        rare_value: str = "rare",
        polynomial_features: bool = False,
        polynomial_degree: int = 2,
        low_variance_threshold: Optional[float] = None,
        group_features: Optional[dict] = None,
        drop_groups: bool = False,
        remove_multicollinearity: bool = False,
        multicollinearity_threshold: float = 0.9,
        bin_numeric_features: Optional[List[str]] = None,
        remove_outliers: bool = False,
        outliers_method: str = "iforest",
        outliers_threshold: float = 0.05,
        fix_imbalance: bool = False,
        fix_imbalance_method: Union[str, Any] = "SMOTE",
        transformation: bool = False,
        transformation_method: str = "yeo-johnson",
        normalize: bool = False,
        normalize_method: str = "zscore",
        pca: bool = False,
        pca_method: str = "linear",
        pca_components: Optional[Union[int, float, str]] = None,
        feature_selection: bool = False,
        feature_selection_method: str = "classic",
        feature_selection_estimator: Union[str, Any] = "lightgbm",
        n_features_to_select: Union[int, float] = 0.2,
        custom_pipeline: Optional[Any] = None,
        custom_pipeline_position: int = -1,
        data_split_shuffle: bool = True,
        data_split_stratify: Union[bool, List[str]] = True,
        fold_strategy: Union[str, Any] = "stratifiedkfold",
        fold: int = 10,
        fold_shuffle: bool = False,
        fold_groups: Optional[Union[str, DataFrame]] = None,
        n_jobs: Optional[int] = -1,
        use_gpu: bool = False,
        html: bool = True,
        session_id: Optional[int] = None,
        system_log: Union[bool, str] = True,
        log_experiment: Union[bool, str, List[Union[str]]] = False,
        experiment_name: Optional[str] = None,
        experiment_custom_tags: Optional[Dict[str, Any]] = None,
        log_plots: Union[bool, list] = False,
        log_profile: bool = False,
        log_data: bool = False,
        verbose: bool = True,
        memory: Union[bool, str] = True,
        profile: bool = False,
        profile_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        if create_date_columns is None:
            create_date_columns = ["day", "month", "year"]

        setup(
            data=data,
            data_func=data_func,
            target=target,
            index=index,
            train_size=train_size,
            test_data=test_data,
            ordinal_features=ordinal_features,
            numeric_features=numeric_features,
            categorical_features=categorical_features,
            date_features=date_features,
            text_features=text_features,
            ignore_features=ignore_features,
            keep_features=keep_features,
            preprocess=preprocess,
            create_date_columns=create_date_columns,
            imputation_type=imputation_type,
            numeric_imputation=numeric_imputation,
            categorical_imputation=categorical_imputation,
            iterative_imputation_iters=iterative_imputation_iters,
            numeric_iterative_imputer=numeric_iterative_imputer,
            categorical_iterative_imputer=categorical_iterative_imputer,
            text_features_method=text_features_method,
            max_encoding_ohe=max_encoding_ohe,
            encoding_method=encoding_method,
            rare_to_value=rare_to_value,
            rare_value=rare_value,
            polynomial_features=polynomial_features,
            polynomial_degree=polynomial_degree,
            low_variance_threshold=low_variance_threshold,
            group_features=group_features,
            drop_groups=drop_groups,
            remove_multicollinearity=remove_multicollinearity,
            multicollinearity_threshold=multicollinearity_threshold,
            bin_numeric_features=bin_numeric_features,
            remove_outliers=remove_outliers,
            outliers_method=outliers_method,
            outliers_threshold=outliers_threshold,
            fix_imbalance=fix_imbalance,
            fix_imbalance_method=fix_imbalance_method,
            transformation=transformation,
            transformation_method=transformation_method,
            normalize=normalize,
            normalize_method=normalize_method,
            pca=pca,
            pca_method=pca_method,
            pca_components=pca_components,
            feature_selection=feature_selection,
            feature_selection_method=feature_selection_method,
            feature_selection_estimator=feature_selection_estimator,
            n_features_to_select=n_features_to_select,
            custom_pipeline=custom_pipeline,
            custom_pipeline_position=custom_pipeline_position,
            data_split_shuffle=data_split_shuffle,
            data_split_stratify=data_split_stratify,
            fold_strategy=fold_strategy,
            fold=fold,
            fold_shuffle=fold_shuffle,
            fold_groups=fold_groups,
            n_jobs=n_jobs,
            use_gpu=use_gpu,
            html=html,
            session_id=session_id,
            system_log=system_log,
            log_experiment=log_experiment,
            experiment_name=experiment_name,
            experiment_custom_tags=experiment_custom_tags,
            log_plots=log_plots,
            log_profile=log_profile,
            log_data=log_data,
            verbose=verbose,
            memory=memory,
            profile=profile,
            profile_kwargs=profile_kwargs,
        )

        self.best_model = None

    def train(self):
        self.best_model = compare_models()
        return finalize_model(self.best_model)

    def model_eval(self):
        return evaluate_model(self.best_model)

    def predict(self, data: DATAFRAME_LIKE = None):
        predict_model(self.best_model, data=data)
