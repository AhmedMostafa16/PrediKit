from ._base import Encoder
from sklearn.preprocessing import (
    OneHotEncoder,
    LabelEncoder,
    OrdinalEncoder

)
from category_encoders import (
    HashingEncoder,
    SumEncoder,
    HelmertEncoder,
    BaseNEncoder,
    CountEncoder
)

class CategoricalEncoder(Encoder):
    """
    A class for categorical feature encoding using various strategies.

    Methods:
        - _onehot_encoder(**kwargs): Returns an instance of OneHotEncoder with the specified parameters.
        - _label_encoder(**kwargs): Returns an instance of LabelEncoder with the specified parameters.
        - _hashing_encoder(**kwargs): Returns an instance of HashingEncoder with the specified parameters.
        - _sum_encoder(**kwargs): Returns an instance of SumEncoder with the specified parameters.
        - _helmert_encoder(**kwargs): Returns an instance of HelmertEncoder with the specified parameters.
        - _base_n_encoder(**kwargs): Returns an instance of BaseNEncoder with the specified parameters.
        - _count_encoder(**kwargs): Returns an instance of CountEncoder with the specified parameters.

    Note:
        - This class extends the 'Encoder' class and provides methods for different categorical encoding strategies.
    """
    
    def _onehot_encoder(self, **kwargs):
        return OneHotEncoder(**kwargs)
    
    def _label_encoder(self, **kwargs):
        return LabelEncoder(**kwargs)
    
    def _hashing_encoder(self, **kwargs):
        return HashingEncoder(**kwargs)
    
    def _sum_encoder(self, **kwargs):
        return SumEncoder(**kwargs)
    
    def _helmert_encoder(self, **kwargs):
        return HelmertEncoder(**kwargs)
    
    def _base_n_encoder(self, **kwargs):
        return BaseNEncoder(**kwargs)
    
    def _count_encoder(self, **kwargs):
        return CountEncoder(**kwargs)



class BinaryEncoder(Encoder):
    """
    A class for binary feature encoding using the ordinal encoding strategy.

    Methods:
        - _ordinal_encoder(**kwargs): Returns an instance of OrdinalEncoder with the specified parameters.

    Note:
        - This class extends the 'Encoder' class and provides a method for binary feature encoding.
    """
    
    def _ordinal_encoder(self, **kwargs):
        return OrdinalEncoder(**kwargs)
