from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    SliderInput,
)
from ...properties.outputs import ImageOutput

@NodeFactory.register("predikit:image:gamma")
class Gamma(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Adjusts the gamma of an input image."
        self.inputs = [
            ImageInput(),
            SliderInput(
                "Gamma",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
        ]
        self.outputs = [
            ImageOutput(image_type=expression.Image(size_as="Input0"))
        ]
        self.category = ImageAdjustmentCategory
        self.name = "Gamma"
        self.icon = "ImGamma"
        self.sub = "Adjustment"

    def run(
        self,
        img: np.ndarray,
        gamma: float,
    ) -> np.ndarray:
        adjusted_image = cv2.pow(img, gamma)
        return adjusted_image
