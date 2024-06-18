from __future__ import annotations
###############################################

import cv2
import numpy as np
###############################################
from ...node_factory import NodeFactory
from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    NumberInput,
    )
from ...properties.outputs import ImageOutput
from ...properties import expression
###############################################

@NodeFactory.register("predikit:image:blur_gauss")
class BlurGauss(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Apply Gaussian blur to an image."
        self.inputs = [
            ImageInput(label="Input Image"),
            NumberInput(label="Size"),
        ]
        self.outputs = [
            ImageOutput(size_as="Input0")
        ]
        self.category = ImageFilterCategory
        self.name = "Blur Gauss"
        self.icon = "ImBlurGauss"
        self.sub = "Filters"

    def run(
            self,
            input_image: np.ndarray,
            size: int,
    ) -> np.ndarray: 
        blurred_image = cv2.GaussianBlur(input_image, (size, size), 0)
        return blurred_image