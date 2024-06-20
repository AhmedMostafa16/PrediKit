from __future__ import annotations

import cv2
import numpy as np

from . import category as ImageFilterCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties import expression
from ...properties.inputs import (
    ImageInput,
    NumberInput,
)
from ...properties.outputs import ImageOutput
from ...utils.image_utils import normalize_normals
from ...utils.utils import get_h_w_c


@NodeFactory.register("predikit:image:normal_addition")
class NormalAddition(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Add 2 normal maps together. Only the R and G channels of the input image will be used. The output normal map is guaranteed to be normalized."
        self.inputs = [
            ImageInput(
                label="image",
            ),
        ]
        self.outputs = [
            ImageOutput(image_type=expression.Image(channels_as="Input0"))
        ]
        self.category = ImageFilterCategory
        self.name = "Normal Addition"
        self.icon = "MdAddCircleOutline"
        self.sub = "Filters"

    def run(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        _, _, c = get_h_w_c(image)
        if c == 3:
            R, G, _ = cv2.split(image)
            R_out, G_out, B_out = normalize_normals(R, G)
            normalized_image = cv2.merge([R_out, G_out, B_out])
        elif c == 4:
            R, G, _, A = cv2.split(image)
            R_out, G_out, B_out = normalize_normals(R, G)
            normalized_image = cv2.merge([R_out, G_out, B_out, A])

        return normalized_image
