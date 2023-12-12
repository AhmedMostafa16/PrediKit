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

from ._base import CategoricalEncodingStrategies

ENCODERS = {
    CategoricalEncodingStrategies.HashingEncoder: HashingEncoder,
    CategoricalEncodingStrategies.SumEncoder: SumEncoder,
    CategoricalEncodingStrategies.BackwardDifferenceEncoder: BackwardDifferenceEncoder,
    CategoricalEncodingStrategies.OneHotEncoder: OneHotEncoder,
    CategoricalEncodingStrategies.HelmertEncoder: HelmertEncoder,
    CategoricalEncodingStrategies.BaseNEncoder: BaseNEncoder,
    CategoricalEncodingStrategies.CountEncoder: CountEncoder,
    CategoricalEncodingStrategies.LabelEncoder: LabelEncoder,
    CategoricalEncodingStrategies.PolynomialEncoder: PolynomialEncoder,
    CategoricalEncodingStrategies.OrdinalEncoder: OrdinalEncoder,
}


def init_encoder(strategy: CategoricalEncodingStrategies, **params):
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
