from __future__ import annotations
################################################

from PIL import Image
import numpy as np
###############################################

from ...node_factory import NodeFactory
from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    NumberInput,
    )
from ...properties.outputs import ImageOutput
###############################################

@NodeFactory.register("predikit:image:resize_to_size")
class ResizeToSize(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Resize an image to a given side length while keeping aspect ratio."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Side Length"),  
        ]
        self.outputs = [
            ImageOutput(channels_as="Input0")
        ]
        self.category = ImageDimensionCategory
        self.name = "Resize To Size"
        self.icon = "ImResizeToSize"
        self.sub = "dimensions"

    def run(
            self,
            image: np.ndarray,
            side_length: int,
    ) -> np.ndarray: 
        pil_image = Image.fromarray(image)
        aspect_ratio = pil_image.width / pil_image.height
        if pil_image.width > pil_image.height:
            new_size = (side_length, int(side_length / aspect_ratio))
        else:
            new_size = (int(side_length * aspect_ratio), side_length)
        if side_length < min(pil_image.width, pil_image.height):
            resized_image = pil_image.resize(new_size, Image.BOX)
        else:
            resized_image = pil_image.resize(new_size, Image.LANCZOS)
        return np.array(resized_image)