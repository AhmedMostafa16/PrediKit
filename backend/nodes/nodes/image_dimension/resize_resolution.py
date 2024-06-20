from __future__ import annotations

from PIL import Image
import numpy as np

from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput
from ...properties import expression
###############################################

@NodeFactory.register("predikit:image:resize_resolution")
class ResizeResolution(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Resize an image to an exact resolution."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Width"),
            NumberInput(label="Height"),
        ]
        self.outputs = [
            ImageOutput(image_type=expression.Image(channels_as="Input0"))#width_as = "input1" , height_as = "input2"
        ]
        self.category = ImageDimensionCategory
        self.name = "Resize Resolution"
        self.icon = "ImResizeResolution"
        self.sub = "dimensions"

    def run(
        self,
        image: np.ndarray,
        width: int,
        height: int,
    ) -> np.ndarray:
        pil_image = Image.fromarray(image)
        new_size = (width, height)
        if width < pil_image.width or height < pil_image.height:
            resized_image = pil_image.resize(new_size, Image.BOX)
        else:
            resized_image = pil_image.resize(new_size, Image.LANCZOS)
        return resized_image
