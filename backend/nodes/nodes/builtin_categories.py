from .dataset import category as DatasetCategory
from .image import category as ImageCategory
from .image_adjustment import category as ImageAdjustmentCategory
from .image_channel import category as ImageChannelCategory
from .image_dimension import category as ImageDimensionCategory
from .image_filter import category as ImageFilterCategory
from .image_utility import category as ImageUtilityCategory
from .utility import category as UtilityCategory
from .visualization import category as VisualizationCategory

builtin_categories = [
    DatasetCategory,
    VisualizationCategory,
    ImageCategory,
    ImageAdjustmentCategory,
    ImageChannelCategory,
    ImageDimensionCategory,
    ImageFilterCategory,
    ImageUtilityCategory,
    UtilityCategory,
]
category_order = [x.name for x in builtin_categories]
