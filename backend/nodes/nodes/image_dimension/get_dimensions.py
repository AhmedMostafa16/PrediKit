from __future__ import annotations
################################################

from typing import Tuple
import numpy as np
###############################################
from ...node_factory import NodeFactory
from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    )
from ...properties.outputs import NumberOutput
from ...utils.utils import get_h_w_c
###############################################
@NodeFactory.register("predikit:image:get_dimensions")
class GetDimensions(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Get the Height, Width, and number of Channels from an image."
        self.inputs = [
            ImageInput(),
        ]
        self.outputs = [
            NumberOutput(label="Height"),
            NumberOutput(label="Width"),
            NumberOutput(label="Channels"),
        ]
        self.category = ImageDimensionCategory
        self.name = "Get Dimensions"
        self.icon = "ImGetDimensions"
        self.sub = "dimensions"

    def run(
            self,
            image: np.ndarray,
    ) -> Tuple[int, int, int]: 
        height, width, channels = get_h_w_c(image)
        return height, width, channels