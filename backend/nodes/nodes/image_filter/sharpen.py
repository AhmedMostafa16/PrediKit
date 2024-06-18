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

@NodeFactory.register("predikit:image:sharpen")
class Sharpen(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Apply sharpening to an image using an unsharp mask."
        self.inputs = [
            ImageInput(label="Input Image"),
        ]
        self.outputs = [
            ImageOutput(size_as="Input0")
        ]
        self.category = ImageFilterCategory
        self.name = "Sharpen"
        self.icon = "ImSharpen"
        self.sub = "Filters"

    def run(
            self,
            input_image: np.ndarray,
    ) -> np.ndarray: 
        
        ###copy past ###

        # Create the kernel for the unsharp mask
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

        # Apply the unsharp mask to the input image
        sharpened_image = cv2.filter2D(input_image, -1, kernel)

        return sharpened_image
