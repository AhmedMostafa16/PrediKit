from __future__ import annotations

import cv2
import numpy as np

from ...node_factory import NodeFactory
from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput
from ...properties import expression


@NodeFactory.register("predikit:image:normal_addition")
class NormalAddition(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Add 2 normal maps together. Only the R and G channels of the input image will be used. The output normal map is guaranteed to be normalized."
        self.inputs = [
            ImageInput(label="Input Normal Map 1"),
            ImageInput(label="Input Normal Map 2"),
        ]
        self.outputs = [
            ImageOutput(image_type=expression.Image(size_as="Input0"))
        ]
        self.category = ImageFilterCategory
        self.name = "Normal Addition"
        self.icon = "ImNormalAddition"
        self.sub = "Filters"

    def run(
            self,
            input_normal_map: np.ndarray,
    ) -> np.ndarray: 
        
        normal_map = input_normal_map[:, :, :2]
        normalized_normal_map = cv2.normalize(normal_map, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        return normalized_normal_map