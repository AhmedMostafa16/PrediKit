from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ColorspaceInput,
    ImageInput,
)
from ...properties.outputs import ImageOutput
from ...utils.color_transfer import color_transfer


@NodeFactory.register("predikit:image:color_transfer")
class ColorTransfer(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Transfers colors from the reference image. 
        Different combinations of settings may perform better for different images. 
        Try multiple setting combinations to find the best results."""
        self.inputs = [
            ImageInput(label="Input Image"),
            ImageInput(label="Reference Image"),
            ColorspaceInput(label="Colorspace"),
        ]
        self.outputs = [
            ImageOutput(image_type=expression.Image(size_as="Input0"))
        ]
        self.category = ImageFilterCategory
        self.name = "Color Transfer"
        self.icon = "ImColorTransfer"
        self.sub = "Filters"

    def run(
        self,
        input_image: np.ndarray,
        reference_image: np.ndarray,
        colorspace: str,
    ) -> np.ndarray:
        return color_transfer(input_image, reference_image, colorspace)
