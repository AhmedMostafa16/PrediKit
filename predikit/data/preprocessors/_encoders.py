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

cat_encoders = {
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
    encoder = cat_encoders.get(strategy)
    if encoder is None:
        raise TypeError(f"Unknown encoder strategy: {strategy}")
    return encoder(**params)
