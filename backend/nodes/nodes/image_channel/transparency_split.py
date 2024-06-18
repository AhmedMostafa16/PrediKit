from __future__ import annotations

from typing import Tuple

import cv2
import numpy as np

from . import category as ImageChannelCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import ImageInput
from ...properties.outputs import ImageOutput

###############################################


###############################################


###############################################


@NodeFactory.register("predikit:image:transparency_split")
class TransparencySplit(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Split image channels into separate channels. 
            Typically used for splitting off an alpha (transparency) layer."""
        self.inputs = [
            ImageInput(
                image_type=expression.Image(channels=4)  # expected image is RGBA
            ),
        ]
        self.outputs = [
            ImageOutput(label="RGB image", channels=3),
            ImageOutput(label="Alpha Channel", channels=1),
        ]
        self.category = ImageChannelCategory
        self.name = "Transparency Split"
        self.icon = "ImTransparencySplit"
        self.sub = "Channels"

    def run(
        self,
        rgba_image: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        red_channel, green_channel, blue_channel, alpha_channel = cv2.split(rgba_image)
        rgb_image = cv2.merge([red_channel, green_channel, blue_channel])
        return rgb_image, alpha_channel
