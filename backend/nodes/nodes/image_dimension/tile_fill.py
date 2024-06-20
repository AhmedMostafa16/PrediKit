from __future__ import annotations

from PIL import Image
import numpy as np

from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    ImageInput,
    NumberInput,
    TileModeInput,
    )
from ...properties.outputs import ImageOutput
from ...properties import expression
from ...utils.tile_util import tile_image
###############################################

@NodeFactory.register("predikit:image:tile_fill")
class TileFill(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Tiles an image to an exact resolution."
        self.inputs = [
            ImageInput(),
            NumberInput("Width", minimum=1, default=1, unit="px"),
            NumberInput("Height", minimum=1, default=1, unit="px"),
            TileModeInput(),  
        ]
        self.outputs = [
            ImageOutput(
                image_type=expression.Image(
                    channels_as="Input0",
                    width="Input1",
                    height="Input2",
                    )
                )
        ]
        self.outputs = [ImageOutput(channels_as="Input0")]
        self.category = ImageDimensionCategory
        self.name = "Tile Fill"
        self.icon = "ImTileFill"
        self.sub = "dimensions"

def run(
        self,
        img: np.ndarray, 
        width: int, 
        height: int, 
        tile_mode: int
    ) -> np.ndarray:
        return tile_image(img, width, height, tile_mode)