from __future__ import annotations
###############################################

import cv2
import numpy as np
###############################################
from ...node_factory import NodeFactory
from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...properties.inputs import (
    ImageInput,
    )
from ...properties.outputs import ImageOutput
from ...properties import expression
###############################################
@NodeFactory.register("predikit:image:average_color_fix")
class AverageColorFix(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Correct for upscaling model color shift by matching average color
             of Input Image to that of a smaller Reference Image."""
        self.inputs = [
            ImageInput(label="Input Image"),
            ImageInput(label="Reference Image"),
        ]
        self.outputs = [
            ImageOutput(size_as="Input0")
        ]
        self.category = ImageFilterCategory
        self.name = "Average Color Fix"
        self.icon = "ImAverageColorFix"
        self.sub = "Filters"

    def run(
            self,
            input_image: np.ndarray,
            reference_image: np.ndarray,
            ) -> np.ndarray:
        input_avg_color = cv2.mean(input_image)[:3]
        reference_avg_color = cv2.mean(reference_image)[:3]
        color_difference = np.subtract(reference_avg_color, input_avg_color)
        corrected_image = cv2.add(input_image, color_difference)
        corrected_image = cv2.convertScaleAbs(corrected_image)

        return corrected_image