from __future__ import annotations

import numpy as np

from . import category as ImageAdjustmentCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    ImageInput,
    SliderInput,
)
from ...properties.outputs import ImageOutput
from ...utils.utils import get_h_w_c


@NodeFactory.register("predikit:image:brightness_and_contrast")
class BrightnessAndContrastNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Adjust the brightness and contrast of an image."
        self.inputs = [
            ImageInput(),
            SliderInput(
                label="Brightness",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
            SliderInput(
                label="Contrast",
                minimum=-100,
                maximum=100,
                default=0,
                precision=1,
                controls_step=1,
            ),
        ]
        self.outputs = [ImageOutput(image_type="Input0")]
        self.category = ImageAdjustmentCategory
        self.name = "Brightness & Contrast"
        self.icon = "ImBrightnessContrast"
        self.sub = "Adjustments"

    def run(
        self, img: np.ndarray, brightness: float, contrast: float
    ) -> np.ndarray:
        brightness /= 100
        contrast /= 100

        if brightness == 0 and contrast == 0:
            return img

        _, _, c = get_h_w_c(img)

        # Contrast correction factor
        max_c: float = 259 / 255
        factor: float = (max_c * (contrast + 1)) / (max_c - contrast)
        add: float = factor * brightness + 0.5 * (1 - factor)

        def process_rgb(rgb: np.ndarray):
            if factor == 1:
                out = rgb + add
            else:
                out = factor * rgb
                out += add

            if add < 0 or factor + add > 1:
                out = np.clip(out, 0, 1, out=out)

            return out

        if c <= 3:
            return process_rgb(img)

        return np.dstack([process_rgb(img[:, :, :3]), img[:, :, 3:]])
