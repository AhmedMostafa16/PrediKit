from __future__ import annotations
################################################

from PIL import Image
import numpy as np
###############################################

from ...node_factory import NodeFactory
from . import category as ImageDimensionCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    NumberInput,
    )
from ...properties.outputs import ImageOutput
###############################################

@NodeFactory.register("predikit:image:tile_fill")
class TileFill(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Tiles an image to an exact resolution."
        self.inputs = [
            ImageInput(),
            NumberInput(label="Width"),  
            NumberInput(label="Height"),  
        ]
        self.outputs = [
            ImageOutput(channels_as="Input0")
        ]
        self.category = ImageDimensionCategory
        self.name = "Tile Fill"
        self.icon = "ImTileFill"
        self.sub = "dimensions"

    def run(
            self,
            image: np.ndarray,
            width: int,
            height: int,
    ) -> np.ndarray: 
        ####copypasted without understaning this code####
        pil_image = Image.fromarray(image)
        new_image = Image.new('RGB', (width, height))
        for i in range(0, width, pil_image.width):
            for j in range(0, height, pil_image.height):
                new_image.paste(pil_image, (i, j))
        return np.array(new_image)