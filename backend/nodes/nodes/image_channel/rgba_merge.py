from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageChannelCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import ImageInput
from ...properties.outputs import ImageOutput

@NodeFactory.register("predikit:image:rgba_merge")
class TransparencyMerge(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Merge image channels together into a ≤4 channel image.
          Typically used for combining an image with an alpha layer."""
        self.inputs = [
            ImageInput("Channel(s) A"),
            ImageInput("Channel(s) B").make_optional(),
            ImageInput("Channel(s) C").make_optional(),
            ImageInput("Channel(s) D").make_optional(),
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(
                    size_as="Input0",
                    channels="""
                    match (
                        Input0.channels
                        + match Input1 { Image as i => i.channels, _ => 0 }
                        + match Input2 { Image as i => i.channels, _ => 0 }
                        + match Input3 { Image as i => i.channels, _ => 0 }
                    ) {
                        1 => 1,
                        2 | 3 => 3,
                        int(4..) => 4
                    }
                    """,
                )
            )
        ]
        self.category = ImageChannelCategory
        self.name = "RGBA Merge"
        self.icon = "ImRGBAMerge"
        self.sub = "Channels"

    def run(
        self,
        channel_a: np.ndarray,
        channel_b: np.ndarray,
        channel_c: np.ndarray,
        channel_d: np.ndarray,
    ) -> np.ndarray:
        image = cv2.merge([channel_a, channel_b, channel_c, channel_d])
        return image
