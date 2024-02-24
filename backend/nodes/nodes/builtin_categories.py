from .dataset import category as DatasetCategory
from .utility import category as UtilityCategory


builtin_categories = [
    DatasetCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]
