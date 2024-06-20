from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageDimensionCategory
from ...node_base import NodeBase

###############################################
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput

###############################################


###############################################
@NodeFactory.register("predikit:image:crop_offsets")
class CropOffsets(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Crop an image based on offset from the top-left corner and the wanted resolution."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Offset X"),
            NumberInput(label="Offset Y"),
            NumberInput(label="Crop Width"),
            NumberInput(label="Crop Height"),
            # input1+input3 < input0.width , input2+input4 < input0.height
        ]
        self.outputs = [ImageOutput(image_type=expression.Image(channels_as="Input0"))]
        self.category = ImageDimensionCategory
        self.name = "Crop Offsets"
        self.icon = "MdCrop"
        self.sub = "dimensions"

    def run(
        self,
        image: np.ndarray,
        offset_x: int,
        offset_y: int,
        crop_width: int,
        crop_height: int,
    ) -> np.ndarray:
        cropped_image = image[
            offset_y : offset_y + crop_height, offset_x : offset_x + crop_width
        ]
        return cropped_image
