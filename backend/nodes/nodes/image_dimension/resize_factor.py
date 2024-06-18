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

################################################


###############################################


###############################################


@NodeFactory.register("predikit:image:resize_factor")
class ResizeFactor(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Resize an image by a percent scale factor."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Scale Factor"),
        ]
        self.outputs = [ImageOutput(channels_as="Input0")]
        self.category = ImageDimensionCategory
        self.name = "Resize Factor"
        self.icon = "ImResizeFactor"
        self.sub = "dimensions"

    def run(
        self,
        image: np.ndarray,
        scale_factor: float,
    ) -> np.ndarray:
        pil_image = Image.fromarray(image)
        new_size = (
            int(pil_image.width * scale_factor),
            int(pil_image.height * scale_factor),
        )
        if scale_factor < 1.0:
            resized_image = pil_image.resize(new_size, Image.BOX)
        else:
            resized_image = pil_image.resize(new_size, Image.LANCZOS)
        return resized_image
