from __future__ import annotations
from typing import Tuple
import cv2
import numpy as np

from ...node_factory import NodeFactory
from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput
from ...properties import expression

@NodeFactory.register("predikit:image:crop_border")
class CropBorder(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Crop an image based on a constant border margin around the entire image."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Border Width")#max = the samllest dimension of the image/2 , min = 0 , default = 0 
        ]
        self.outputs = [
            ImageOutput(
                channels_as="Input0"
                #image_type=expression.Image() #width_as = "input0.width - input1" , height_as = "input0.height - input1"
            )
        ]
        self.category = ImageDimensionCategory
        self.name = "Crop Border"
        self.icon = "ImCropBorder"
        self.sub = "dimensions"
    def run(
            self,
            image: np.ndarray,
            border_width: int
            ) -> np.ndarray: 
        cropped_image = image[border_width:-border_width, border_width:-border_width]
        return cropped_image,