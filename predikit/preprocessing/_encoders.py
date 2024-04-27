import numpy as np
from pandas import DataFrame
import hashlib
from collections import defaultdict

from category_encoders import (
    BackwardDifferenceEncoder,
    BaseNEncoder,
    CountEncoder,
    HashingEncoder,
    HelmertEncoder,
    PolynomialEncoder,
    SumEncoder,
)
from sklearn.preprocessing import (
    LabelEncoder,
    # OneHotEncoder,
    OrdinalEncoder,
)

from ._base import EncodingStrategies, Encoder


class OneHotEncoder:
    def __init__(self, cols: list[str] = None, drop: str = None) -> None:
        self.columns: list[str] = cols
        self.drop: str = drop
        self.encodings: dict[str, int] = {}
        self.feature_names_out: list[str] = []

    def fit(self, df: DataFrame) -> None:
        if self.columns is None:
            self.columns = df.columns
        for column in self.columns:
            unique_values = df[column].unique()
            if self.drop == "first":
                unique_values = np.delete(
                    unique_values, 0
                )  # Drop the first category
            elif self.drop == "if_binary" and len(unique_values) == 2:
                unique_values = unique_values[
                    1:
                ]  # Drop the first category if binary
            self.encodings[column] = {
                value: np.eye(len(unique_values))[i]
                for i, value in enumerate(unique_values)
            }
            self.feature_names_out.extend(
                [f"{column}_{value}" for value in unique_values]
            )

    def transform(self, df: DataFrame) -> DataFrame:
        df_encoded = df
        for column in self.columns:
            if (
                column in df_encoded
            ):  # Check if column exists after dropping (if_binary)
                for value, _ in self.encodings[column].items():
                    df_encoded[column + "_" + str(value)] = (
                        df_encoded[column] == value
                    ).astype(int)
                df_encoded.drop(column, axis=1, inplace=True)
        return df_encoded

    def fit_transform(self, df: DataFrame) -> DataFrame:
        self.fit(df)
        return self.transform(df)

    def get_features_names_out(self) -> list[str]:
        """
        Returns the names of the encoded features.

        This method should be called after fitting the encoder.

        Returns:
            list: A list of string, the names of the encoded features.
        """
        if self.feature_names_out is None:
            raise ValueError(
                "Please fit the encoder before calling get_features_names_out."
            )
        return self.feature_names_out


class EncoderFetch:
    _ENCODERS: dict[EncodingStrategies, Encoder] = {
        EncodingStrategies.HashingEncoder: HashingEncoder,
        EncodingStrategies.SumEncoder: SumEncoder,
        EncodingStrategies.BackwardDifferenceEncoder: BackwardDifferenceEncoder,
        EncodingStrategies.HelmertEncoder: HelmertEncoder,
        EncodingStrategies.BaseNEncoder: BaseNEncoder,
        EncodingStrategies.CountEncoder: CountEncoder,
        EncodingStrategies.LabelEncoder: LabelEncoder,
        EncodingStrategies.PolynomialEncoder: PolynomialEncoder,
        EncodingStrategies.OrdinalEncoder: OrdinalEncoder,
    }

    def __init__(
        self,
        strategy: EncodingStrategies,
        cols: list[str] = None,
        **encoder_params,
    ) -> None:
        self.strategy = strategy
        self.columns = cols
        self.encoder_params = encoder_params
        self._encoder = self._ENCODERS[self.strategy](**self.encoder_params)

    def fit(self, df: DataFrame) -> None:
        if self.columns is None:
            self.columns = df.columns
        self._encoder.fit(df[self.columns])

    def transform(self, df: DataFrame) -> DataFrame:
        df_encoded = df.copy()
        if self.strategy in [
            EncodingStrategies.OrdinalEncoder,
            EncodingStrategies.LabelEncoder,
        ]:
            df_encoded = DataFrame(
                self._encoder.transform(df_encoded[self.columns])
            )
            df.drop(self.columns, axis=1, inplace=True)
            df[df_encoded.columns] = df_encoded
        else:
            cat_col = [
                col
                for col in self.columns
                if col
                in df_encoded.select_dtypes(include=["category", "object"])
            ]
            df_encoded = self._encoder.transform(df_encoded[self.columns])
            df[df_encoded.columns] = df_encoded
            df.drop(cat_col, axis=1, inplace=True)
        return df

    def fit_transform(self, df: DataFrame):
        self.fit(df)
        return self.transform(df)


# ENCODERS = {
#     EncodingStrategies.HashingEncoder: HashingEncoder,
#     EncodingStrategies.SumEncoder: SumEncoder,
#     EncodingStrategies.BackwardDifferenceEncoder: BackwardDifferenceEncoder,
#     EncodingStrategies.OneHotEncoder: OneHotEncoder,
#     EncodingStrategies.HelmertEncoder: HelmertEncoder,
#     EncodingStrategies.BaseNEncoder: BaseNEncoder,
#     EncodingStrategies.CountEncoder: CountEncoder,
#     EncodingStrategies.LabelEncoder: LabelEncoder,
#     EncodingStrategies.PolynomialEncoder: PolynomialEncoder,
#     EncodingStrategies.OrdinalEncoder: OrdinalEncoder,
# }
ENCODERS = {
    EncodingStrategies.HashingEncoder: EncoderFetch,
    EncodingStrategies.SumEncoder: EncoderFetch,
    EncodingStrategies.BackwardDifferenceEncoder: EncoderFetch,
    EncodingStrategies.OneHotEncoder: OneHotEncoder,
    EncodingStrategies.HelmertEncoder: EncoderFetch,
    EncodingStrategies.BaseNEncoder: EncoderFetch,
    EncodingStrategies.CountEncoder: EncoderFetch,
    EncodingStrategies.LabelEncoder: EncoderFetch,
    EncodingStrategies.PolynomialEncoder: EncoderFetch,
    EncodingStrategies.OrdinalEncoder: EncoderFetch,
}


def init_encoder(strategy: EncodingStrategies, **params):
    """
    Initialize an encoder based on the specified strategy.

    Parameters
    ----------
    strategy : CategoricalEncodingStrategies
        The encoding strategy to use.
    **params : dict
        Additional parameters to pass to the encoder constructor.

    Returns
    -------
    object
        An instance of the encoder.

    Raises
    ------
    TypeError
        If the specified strategy is not supported.
    """
    encoder = ENCODERS.get(strategy)
    if encoder is None:
        raise TypeError(f"Unsupported encoding strategy: {strategy}")
    if encoder is EncoderFetch:
        return encoder(strategy, **params)
    else:
        return encoder(**params)


class HashingEncoder:
    def __init__(self, cols, hash_func=hashlib.md5):
        """
        Initializes the encoder.

        Args:
        cols (list): A list of column names to encode.
        hash_func (function, optional): The hashing function to use. Defaults to hashlib.md5.
        """

        self.cols = cols
        self.hash_func = hash_func
        self.n_components = 10  # Set a default value for n_components
        self.encoders = {}

    def fit(self, df):
        """
        Learns the relationships between values in the specified columns.

        Args:
                df (pandas.DataFrame): The DataFrame containing the columns to encode.
        """

        for col in self.cols:
            unique_values = df[col].unique()
            encoder = defaultdict(lambda: self.n_components - 1)
        for value in unique_values:
            hashed_value = self.hash_func(str(value).encode()).hexdigest()[
                : self.n_components
            ]
            encoder[value] = int(hashed_value, 16)
        self.encoders[col] = encoder

    def transform(self, df):
        """
        Encodes the specified columns of the DataFrame using the fitted encoders.

        Args:
                df (pandas.DataFrame): The DataFrame to encode.

        Returns:
                pandas.DataFrame: The DataFrame with encoded columns.
        """
        encoded_df = df
        for col in self.cols:
            encoded_values = []
        for value in df[col]:
            encoded_values.append(self.encoders[col][value])
        encoded_df[f"{col}_encoded"] = encoded_values
        return encoded_df

    def fit_transform(self, df):
        """
            Convenience method that combines fitting and transforming.

        Args:
                df (pandas.DataFrame): The DataFrame to fit and encode.

        Returns:
        pandas.DataFrame: The DataFrame with encoded columns.
        """
        self.fit(df)
        return self.transform(df)
