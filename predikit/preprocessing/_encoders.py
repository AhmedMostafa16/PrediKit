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
    OneHotEncoder,
    OrdinalEncoder,
)

from ._base import EncodingStrategies

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
