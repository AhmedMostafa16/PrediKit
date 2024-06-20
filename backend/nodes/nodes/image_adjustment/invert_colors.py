from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import ImageInput
from ...properties.outputs import ImageOutput

@NodeFactory.register("predikit:image:invert_colors")
class InvertColors(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Invert all colors in the input image."
        self.inputs = [ImageInput()]
        self.outputs = [ImageOutput(image_type=expression.Image(size_as="Input0"))]
        self.category = ImageAdjustmentCategory
        self.name = "Invert Colors"
        self.icon = "ImInvertColors"
        self.sub = "Adjustments"

    def run(
        self,
        img: np.ndarray,
    ) -> np.ndarray:
        adjusted_image = cv2.bitwise_not(img)
        return adjusted_image
