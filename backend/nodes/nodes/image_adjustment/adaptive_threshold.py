from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    AdaptiveMethodInput,
    AdaptiveThresholdInput,
    ImageInput,
    NumberInput,
    SliderInput,
)
from ...properties.outputs import ImageOutput


@NodeFactory.register("predikit:image:adaptive_threshold")
class AdaptiveThreshold(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = """Applies an adaptive threshold to an image. 
            This means the threshold value is determined for each pixel based on a small region around it."""
        self.inputs = [
            ImageInput(image_type=expression.Image(channels=1)),
            SliderInput(
                "Maximum Value",
                maximum=100,
                default=100,
                precision=1,
                controls_step=1,
            ),
            AdaptiveMethodInput(),
            AdaptiveThresholdInput(),
            NumberInput("Block Radius", default=1, minimum=1),
            NumberInput("Mean Subtraction"),
        ]
        self.outputs = [ImageOutput(image_type="Input0")]
        self.name = "Adaptive Threshold"
        self.icon = "ImAdaptiveThreshold"
        self.sub = "Adjustments"

    def run(
        self,
        img: np.ndarray,
        max_value: int,
        adaptive_method: str,
        adaptive_threshold: str,
        block_radius: int,
        mean_subtraction: int,
    ) -> np.ndarray:
        block_size = 2 * block_radius + 1
        thresholded_image = cv2.adaptiveThreshold(
            img,
            max_value,
            adaptive_method,
            adaptive_threshold,
            block_size,
            mean_subtraction,
        )
        return thresholded_image
