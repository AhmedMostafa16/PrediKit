from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase

###############################################
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    SliderInput,
)
from ...properties.outputs import ImageOutput

###############################################


###############################################


@NodeFactory.register("predikit:image:threshold")
class Threshold(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Replaces pixels based on the threshold value. 
            If the pixel value is smaller than the threshold, 
            it is set to 0, otherwise it is set to the maximum value."""
        self.inputs = [
            ImageInput(),
            SliderInput(
                "Threshold",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
        ]
        self.outputs = [ImageOutput(image_type=expression.Image(size_as="Input0"))]

    def run(
        self,
        img: np.ndarray,
        threshold: int,
    ) -> np.ndarray:
        _, thresholded_image = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return thresholded_image
