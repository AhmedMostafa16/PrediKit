from __future__ import annotations
###############################################

import cv2
import numpy as np
###############################################
from ...node_factory import NodeFactory
from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    SliderInput
    )
from ...properties.outputs import ImageOutput
###############################################

@NodeFactory.register("predikit:image:opacity")
class Opacity(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Adjusts the opacity of an image. The higher the opacity value, the more opaque the image is."
        self.inputs = [
            ImageInput(),
            SliderInput(
                "Opacity",
                minimum= 0,
                maximum= 100,
                default= 0,
                precision= 1,
                controls_step= 1,
            ),     
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(size_as="Input0")
            )
        ]
        self.category = ImageAdjustmentCategory
        self.name = "Opacity"
        self.icon = "ImOpacity"
        self.sub = "Adjustments"

    def run(
        self,
        img: np.ndarray,
        opacity: float,
    ) -> np.ndarray:
        overlay = np.zeros_like(img)
        adjusted_image : np.ndarray
        cv2.addWeighted(img, opacity, overlay, 1 - opacity, 0, adjusted_image)
        return adjusted_image