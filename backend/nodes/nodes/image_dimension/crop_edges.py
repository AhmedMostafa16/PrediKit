from __future__ import annotations

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

@NodeFactory.register("predikit:image:crop_edges")
class CropEdges(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Crop an image using separate amounts from each edge."
        self.inputs = [
            ImageInput(),
            NumberInput("Top", unit="px", minimum=None),
            NumberInput("Left", unit="px", minimum=None),
            NumberInput("Right", unit="px", minimum=None),
            NumberInput("Bottom", unit="px", minimum=None),
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(
                    width="(Input0.width - (Input2 + Input3)) & int(1..)",
                    height="(Input0.height - (Input1 + Input4)) & int(1..)",
                    channels_as="Input0",
                )
            ).with_never_reason(
                "The cropped area would result in an image with no width or no height."
            )
        ]
        self.category = ImageDimensionCategory
        self.name = "Crop Edges"
        self.icon = "ImCropEdges"
        self.sub = "dimensions"

    def run(
            self,
            image: np.ndarray,
            top_margin: int,
            bottom_margin: int,
            left_margin: int,
            right_margin: int
            ) -> np.ndarray: 
        # Crop the image
        cropped_image = image[top_margin:-bottom_margin, left_margin:-right_margin]

        return cropped_image,