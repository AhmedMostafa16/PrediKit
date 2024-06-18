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

    def run(
            self,
            input_image: np.ndarray,
            reference_image: np.ndarray,
    ) -> np.ndarray: 
        ###copy past ###
        
        # Convert the images from the RGB to L*a*b* color space
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
        reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2LAB)

        # Compute color statistics for the input and reference images
        (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = self.image_stats(input_image)
        (lMeanRef, lStdRef, aMeanRef, aStdRef, bMeanRef, bStdRef) = self.image_stats(reference_image)

        # Subtract the means from the input image
        (l, a, b) = cv2.split(input_image)
        l -= lMeanSrc
        a -= aMeanSrc
        b -= bMeanSrc

        # Scale by the standard deviations
        l = (lStdRef / lStdSrc) * l
        a = (aStdRef / aStdSrc) * a
        b = (bStdRef / bStdSrc) * b

        # Add in the reference mean
        l += lMeanRef
        a += aMeanRef
        b += bMeanRef

        # Clip the pixel intensities to [0, 255] if they fall outside this range
        l = np.clip(l, 0, 255)
        a = np.clip(a, 0, 255)
        b = np.clip(b, 0, 255)

        # Merge the channels together and convert back to the RGB color space
        transfer_image = cv2.merge([l, a, b])
        transfer_image = cv2.cvtColor(transfer_image.astype("uint8"), cv2.COLOR_LAB2BGR)

        return transfer_image
