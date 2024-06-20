from __future__ import annotations

import numpy as np

from . import category as ImageChannelCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput
from ...utils.fill_alpha import (
    convert_to_binary_alpha,
    fill_alpha_edge_extend,
)


@NodeFactory.register("predikit:image:fill_alpha")
class FillAlpha(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = (
            "Fills the transparent pixels of an image with nearby colors."
        )
        self.inputs = [
            ImageInput(label="Input Image"),
            NumberInput(label="distance", default=1),
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(size_as="Input0", channels=4)
            )
        ]
        self.category = ImageChannelCategory
        self.name = "Fill Alpha"
        self.icon = "ImRGBAMerge"
        self.sub = "Channels"

    def run(
        self,
        image: np.ndarray,
        distance: int,
    ) -> np.ndarray:
        convert_to_binary_alpha(image, threshold=0)
        adjusted_image = fill_alpha_edge_extend(image, distance)
        return adjusted_image
