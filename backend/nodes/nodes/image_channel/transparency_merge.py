from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageChannelCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import ImageInput
from ...properties.outputs import ImageOutput

@NodeFactory.register("predikit:image:transparency_merge")
class TransparencyMerge(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Merge RGB and Alpha (transparency) image channels into 4-channel RGBA channels."""
        self.inputs = [
            ImageInput(
                image_type=expression.Image(channels=3)
            ),
            ImageInput(
                image_type=expression.Image(channels=1)
            ).make_optional(),
        ]
        self.outputs = [ImageOutput(image_type=expression.Image(channels=4))]
        self.category = ImageChannelCategory
        self.name = "Transparency Merge"
        self.icon = "ImTransparencyMerge"
        self.sub = "Channels"

    def run(
        self,
        rgb_image: np.ndarray,
        alpha_channel: np.ndarray,
    ) -> np.ndarray:
        b_channel, g_channel, r_channel = cv2.split(rgb_image)
        rgba_image = cv2.merge([b_channel, g_channel, r_channel, alpha_channel])
        return rgba_image
