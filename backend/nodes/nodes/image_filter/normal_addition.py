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
    NumberInput,
    )
from ...properties.outputs import ImageOutput
from ...properties import expression
###############################################

@NodeFactory.register("predikit:image:color_transfer")
class ColorTransfer(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Transfers colors from the reference image. Different combinations of settings may perform better for different images. Try multiple setting combinations to find the best results."
        self.inputs = [
            ImageInput(label="Input Image"),
            ImageInput(label="Reference Image"),
        ]
        self.outputs = [
            ImageOutput(size_as="Input0")
        ]
        self.category = ImageFilterCategory
        self.name = "Color Transfer"
        self.icon = "ImColorTransfer"
        self.sub = "Filters"

@NodeFactory.register("predikit:image:normal_addition")
class NormalAddition(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Add 2 normal maps together. Only the R and G channels of the input image will be used. The output normal map is guaranteed to be normalized."
        self.inputs = [
            ImageInput(label="Input Normal Map 1"),
            ImageInput(label="Input Normal Map 2"),
        ]
        self.outputs = [
            ImageOutput(size_as="Input0")
        ]
        self.category = ImageFilterCategory
        self.name = "Normal Addition"
        self.icon = "ImNormalAddition"
        self.sub = "Filters"

    def run(
            self,
            input_normal_map_1: np.ndarray,
            input_normal_map_2: np.ndarray,
    ) -> np.ndarray: 
        ####copy past ####
        
        # Extract the R and G channels from the input normal maps
        normal_map_1 = input_normal_map_1[:, :, :2]
        normal_map_2 = input_normal_map_2[:, :, :2]

        # Add the two normal maps together
        added_normal_map = cv2.add(normal_map_1, normal_map_2)

        # Normalize the output normal map
        normalized_normal_map = cv2.normalize(added_normal_map, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

        return normalized_normal_map
