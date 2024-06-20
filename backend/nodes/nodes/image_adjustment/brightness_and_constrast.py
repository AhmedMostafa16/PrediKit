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

@NodeFactory.register("predikit:image:brightness_and_constrast")
class BrightnessAndConstrast(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Adjust the brightness and contrast of the input image."
        self.inputs = [
            ImageInput(),
            SliderInput(
                "Brightness",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
            SliderInput(
                "Contrast",
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
        self.name = "Brightness & Contrast"
        self.icon = "ImBrightnessContrast"
        self.sub = "Adjustments"

    def run(
        self,
        img: np.ndarray,
        brightness: float,
        contrast: float,
    ) -> np.ndarray:
        adjusted_image = cv2.convertScaleAbs(img, alpha=brightness, beta=contrast)
        return adjusted_image
