from .image import category as ImageCategory
from .image_utility import category as ImageUtilityCategory
from .utility import category as UtilityCategory
from .visualization import category as VisualizationCategory
from .dataset import category as DatasetCategory

builtin_categories = [
    DatasetCategory,
    VisualizationCategory,
    ImageCategory,
    ImageUtilityCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]
