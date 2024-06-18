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

###############################################


###############################################


###############################################
@NodeFactory.register("predikit:image:hue_and_saturation")
class HueAndSaturation(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Adjust the hue and saturation of the input image. This is performed in the HSV color-space."
        self.inputs = [
            ImageInput(),
            SliderInput(
                "Saturation Scale",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
            SliderInput(
                "Hue Shift",
                minimum=0,
                maximum=180,
                default=0,
                precision=1,
                controls_step=1,
            ),
        ]
        self.outputs = [ImageOutput(image_type=expression.Image(size_as="Input0"))]
        self.category = ImageAdjustmentCategory
        self.name = "Hue & Saturation"
        self.icon = "ImHueSaturation"
        self.sub = "Adjustments"

    def run(
        self, img: np.ndarray, hue_shift: int, saturation_scale: float
    ) -> np.ndarray:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        h = (h + hue_shift) % 180
        s = cv2.add(s, saturation_scale)
        hsv = cv2.merge([h, s, v])
        adjusted_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted_img
