from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput


@NodeFactory.register("predikit:image:blur_median")
class BlurMedian(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Apply median blur to an image."
        self.inputs = [
            ImageInput(label="Input Image"),
            NumberInput(label="Kernel Size"),
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(
                    size_as="Input0", channels_as="Input0"
                )
            )
        ]
        self.category = ImageFilterCategory
        self.name = "Blur Median"
        self.icon = "ImBlurMedian"
        self.sub = "Filters"

    def run(
        self,
        input_image: np.ndarray,
        kernel_size: int,
    ) -> np.ndarray:
        blurred_image = cv2.medianBlur(input_image, kernel_size)
        return blurred_image
