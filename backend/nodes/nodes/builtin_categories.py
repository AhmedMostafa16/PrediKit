from .dataset import category as DatasetCategory
from .utility import category as UtilityCategory
from .visualization import category as VisualizationCategory

builtin_categories = [
    DatasetCategory,
    VisualizationCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]
