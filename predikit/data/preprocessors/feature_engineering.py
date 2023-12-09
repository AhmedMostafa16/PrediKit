from ._base import FeatureEngineering
import pandas as pd
from ._base import *
from typing import Self
from .encoders import (
    CategoricalEncoder,
    BinaryEncoder
)


class FeatureSelection(FeatureEngineering):
    pass


class NumericalInteractionFeatures(FeatureEngineering):
    pass

class EncodingProcessor(Encoder):

    def __init__(
            self,
            strategy: EncodingStrategies = CategoricalEncodingStrategies.OneHotEncoder,
            **encoder_params
            ):
        self.strategy = strategy
        self.encoder = None
        self.encoder_params = encoder_params
    
    def fit(self, data: pd.DataFrame, cols: list[str] | None = None) -> Self:
        """
        Fit the encoder to the specified columns or the entire DataFrame.

        Parameters:
            - data (pd.DataFrame): The input DataFrame to fit the encoder.
            - cols (list[str] | None): Optional. List of column names to fit the encoder.
                                    If None, the encoder will be fitted to all columns in the DataFrame.

        Returns:
            Self: Returns the instance of the class after fitting the encoder.

        Notes:
            - The method selects a categorical encoding strategy based on the specified strategy attribute.
            - The chosen encoding strategy is applied to the specified columns or the entire DataFrame.
            - The fitted encoder is stored in the 'encoder' attribute of the class.

        Example:
            encoder_instance = MyDataTransformer(strategy=CategoricalEncodingStrategies.OneHotEncoder, encoder_params={})
            encoder_instance.fit(input_data, cols=['col1', 'col2'])
        """
    
        if cols is not None:
            data = data[cols]

        encoder_strategy = {
            CategoricalEncodingStrategies.OneHotEncoder: CategoricalEncoder()._onehot_encoder,
            CategoricalEncodingStrategies.LabelEncoder: CategoricalEncoder()._label_encoder,
            CategoricalEncodingStrategies.HashingEncoder: CategoricalEncoder()._hashing_encoder,
            CategoricalEncodingStrategies.SumEncoder: CategoricalEncoder()._sum_encoder,
            CategoricalEncodingStrategies.HelmertEncoder: CategoricalEncoder()._base_n_encoder,
            CategoricalEncodingStrategies.BaseNEncoder: CategoricalEncoder()._base_n_encoder,
            CategoricalEncodingStrategies.CountEncoder: CategoricalEncoder()._count_encoder,
            BinaryEncodingStrategies.OrdinalEncoder: BinaryEncoder()._ordinal_encoder
        }

        self.encoder = encoder_strategy[self.strategy](**self.encoder_params)
        self.encoder.fit(data)
        return self
    
    def transform(
        self, data: pd.DataFrame, cols: list[str] | None = None
    ) -> pd.DataFrame:
    
        """
        Transform the input DataFrame by encoding specified columns or the entire DataFrame.

        Parameters:
            - data (pd.DataFrame): The input DataFrame to be transformed.
            - cols (list[str] | None): Optional. List of column names to be encoded. 
                                    If None, all columns in the DataFrame will be encoded.

        Returns:
            pd.DataFrame: Transformed DataFrame with encoded features.

        Notes:
            - The method utilizes an encoder (self.encoder) to transform the specified columns or the entire DataFrame.
            - The transformed features are added to the original DataFrame.
            - If 'cols' is not None, the original columns are dropped after encoding.

        Example:
            transformer = MyDataTransformer(encoder_instance)
            transformed_data = transformer.transform(input_data, cols=['col1', 'col2'])
        """
        
        encodeing_data = data[cols] if cols is not None else data

        data[self.encoder.get_feature_names_out()] = self.encoder.transform(encodeing_data)

        if cols is not None:
            data.drop(cols, axis=1, inplace= True)

        return data

    
    def fit_transform(
        self, data: pd.DataFrame, cols: list[str] | None = None
    ) -> Self:
        
        """
        Fit the encoder to the specified columns or the entire DataFrame and transform the data.

        Parameters:
            - data (pd.DataFrame): The input DataFrame to fit the encoder and transform.
            - cols (list[str] | None): Optional. List of column names to fit the encoder.
                                    If None, the encoder will be fitted to all columns in the DataFrame.

        Returns:
            Self: Returns the instance of the class after fitting the encoder and transforming the data.

        Notes:
            - This method combines the 'fit' and 'transform' steps in a single call.
            - The encoder is fitted to the specified columns or the entire DataFrame.
            - The fitted encoder is then applied to transform the input data.
            - The transformed features are added to the original DataFrame.
            - If 'cols' is not None, the original columns are dropped after encoding.

        Example:
            transformer = MyDataTransformer(strategy=CategoricalEncodingStrategies.OneHotEncoder, encoder_params={})
            transformed_data = transformer.fit_transform(input_data, cols=['col1', 'col2'])
        """

        self.fit(data, cols)
        return self.transform(data, cols)
