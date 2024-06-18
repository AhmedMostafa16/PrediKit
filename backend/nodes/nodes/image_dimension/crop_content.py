from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageDimensionCategory
from ...node_base import NodeBase

###############################################
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput

###############################################


###############################################
@NodeFactory.register("predikit:image:crop_content")
class CropContent(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Crop an image to the boundaries of the visible image content, 
            removing borders at or below the given opacity threshold."""
        self.inputs = [ImageInput(), NumberInput(label="Opacity Threshold")]
        self.outputs = [ImageOutput(image_type=expression.Image(channels_as="Input0"))]
        self.category = ImageDimensionCategory
        self.name = "Crop Content"
        self.icon = "ImCropContent"
        self.sub = "dimensions"

    def run(self, image: np.ndarray, opacity_threshold: int) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshed = cv2.threshold(gray, opacity_threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        cropped_image = image[y : y + h, x : x + w]

        return (cropped_image,)
