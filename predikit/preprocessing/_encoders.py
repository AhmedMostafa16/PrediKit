import numpy as np
from pandas import DataFrame

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

from ._base import EncodingStrategies

class OneHotEncoder:
    def __init__(self, cols: list[str] = None, drop: str =None) -> None:
        self.columns: list[str] = cols
        self.encodings: dict[str, int] = {}
        self.drop: str = drop
        self.feature_names_out: list[str] = []

    def fit(self, df) -> None:
        if self.columns is None:
            self.columns = df.columns
        for column in self.columns:
            unique_values = df[column].unique()
            if self.drop == "first":
                unique_values = np.delete(unique_values, 0)  # Drop the first category
            elif self.drop == "if_binary" and len(unique_values) == 2:
                unique_values = unique_values[1:]  # Drop the first category if binary
            self.encodings[column] = {value: np.eye(len(unique_values))[i] for i, value in enumerate(unique_values)}
            self.feature_names_out.extend([f"{column}_{value}" for value in unique_values])

    def transform(self, df) -> DataFrame:
        df_encoded = df
        for column in self.columns:
            if column in df_encoded:  # Check if column exists after dropping (if_binary)
                for value, _ in self.encodings[column].items():
                    df_encoded[column + '_' + str(value)] = (df_encoded[column] == value).astype(int)
                df_encoded.drop(column, axis= 1, inplace = True)
        return df_encoded

    def fit_transform(self, df) -> DataFrame:
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
            raise ValueError("Please fit the encoder before calling get_features_names_out.")
        return self.feature_names_out


ENCODERS = {
    EncodingStrategies.HashingEncoder: HashingEncoder,
    EncodingStrategies.SumEncoder: SumEncoder,
    EncodingStrategies.BackwardDifferenceEncoder: BackwardDifferenceEncoder,
    EncodingStrategies.OneHotEncoder: OneHotEncoder,
    EncodingStrategies.HelmertEncoder: HelmertEncoder,
    EncodingStrategies.BaseNEncoder: BaseNEncoder,
    EncodingStrategies.CountEncoder: CountEncoder,
    EncodingStrategies.LabelEncoder: LabelEncoder,
    EncodingStrategies.PolynomialEncoder: PolynomialEncoder,
    EncodingStrategies.OrdinalEncoder: OrdinalEncoder,
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
    return encoder(**params)

