import cv2
import numpy as np


class BlendModes:
    """Blending mode constants"""

    NORMAL = 0
    MULTIPLY = 1
    DARKEN = 2
    LIGHTEN = 3
    ADD = 4
    COLOR_BURN = 5
    COLOR_DODGE = 6
    REFLECT = 7
    GLOW = 8
    OVERLAY = 9
    DIFFERENCE = 10
    NEGATION = 11
    SCREEN = 12
    XOR = 13
    SUBTRACT = 14
    DIVIDE = 15
    EXCLUSION = 16
    SOFT_LIGHT = 17


__normalized = {
    BlendModes.NORMAL: True,
    BlendModes.MULTIPLY: True,
    BlendModes.DARKEN: True,
    BlendModes.LIGHTEN: True,
    BlendModes.ADD: False,
    BlendModes.COLOR_BURN: False,
    BlendModes.COLOR_DODGE: False,
    BlendModes.REFLECT: False,
    BlendModes.GLOW: False,
    BlendModes.OVERLAY: True,
    BlendModes.DIFFERENCE: True,
    BlendModes.NEGATION: True,
    BlendModes.SCREEN: True,
    BlendModes.XOR: True,
    BlendModes.SUBTRACT: False,
    BlendModes.DIVIDE: False,
    BlendModes.EXCLUSION: True,
    BlendModes.SOFT_LIGHT: True,
}


def blend_mode_normalized(blend_mode: int) -> bool:
    """
    Returns whether the given blend mode is guaranteed to produce normalized results (value between 0 and 1).

    Args:
        blend_mode (int): The blend mode constant.

    Returns:
        bool: True if the blend mode is guaranteed to produce normalized results, False otherwise.
    """
    return __normalized.get(blend_mode, False)


class ImageBlender:
    """Class for compositing images using different blending modes."""

    def __init__(self):
        self.modes = {
            BlendModes.NORMAL: self.__normal,
            BlendModes.MULTIPLY: self.__multiply,
            BlendModes.DARKEN: self.__darken,
            BlendModes.LIGHTEN: self.__lighten,
            BlendModes.ADD: self.__add,
            BlendModes.COLOR_BURN: self.__color_burn,
            BlendModes.COLOR_DODGE: self.__color_dodge,
            BlendModes.REFLECT: self.__reflect,
            BlendModes.GLOW: self.__glow,
            BlendModes.OVERLAY: self.__overlay,
            BlendModes.DIFFERENCE: self.__difference,
            BlendModes.NEGATION: self.__negation,
            BlendModes.SCREEN: self.__screen,
            BlendModes.XOR: self.__xor,
            BlendModes.SUBTRACT: self.__subtract,
            BlendModes.DIVIDE: self.__divide,
            BlendModes.EXCLUSION: self.__exclusion,
            BlendModes.SOFT_LIGHT: self.__soft_light,
        }

    def apply_blend(
        self, a: np.ndarray, b: np.ndarray, blend_mode: int
    ) -> np.ndarray:
        """
        Applies the specified blend mode to two input images.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.
            blend_mode (int): The blend mode constant.

        Returns:
            np.ndarray: The blended image.
        """
        return self.modes[blend_mode](a, b)

    @staticmethod
    def __normal(a: np.ndarray, _: np.ndarray) -> np.ndarray:
        """
        Blending mode: Normal.

        Args:
            a (np.ndarray): The first input image.
            _: Ignored second input image.

        Returns:
            np.ndarray: The blended image (same as the first input image).
        """
        return a

    @staticmethod
    def __multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Multiply.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return a * b

    @staticmethod
    def __darken(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Darken.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.minimum(a, b)

    @staticmethod
    def __lighten(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Lighten.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.maximum(a, b)

    @staticmethod
    def __add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Add.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return a + b

    @staticmethod
    def __color_burn(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Color Burn.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.where(
            a == 0, 0, np.maximum(0, (1 - ((1 - b) / np.maximum(0.0001, a))))
        )

    @staticmethod
    def __color_dodge(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Color Dodge.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.where(
            a == 1, 1, np.minimum(1, b / np.maximum(0.0001, (1 - a)))
        )

    @staticmethod
    def __reflect(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Reflect.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.where(
            a == 1, 1, np.minimum(1, b * b / np.maximum(0.0001, 1 - a))
        )

    @staticmethod
    def __glow(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Glow.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.where(
            b == 1, 1, np.minimum(1, a * a / np.maximum(0.0001, 1 - b))
        )

    @staticmethod
    def __overlay(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Overlay.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return np.where(b < 0.5, (2 * b * a), (1 - (2 * (1 - b) * (1 - a))))

    @staticmethod
    def __difference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Difference.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return cv2.absdiff(a, b)

    @staticmethod
    def __negation(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Negation.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return 1 - cv2.absdiff(1 - b, a)

    @staticmethod
    def __screen(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Screen.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return a + b - (a * b)  # type: ignore

    @staticmethod
    def __xor(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: XOR.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return (
            np.bitwise_xor(
                (a * 255).astype(np.uint8), (b * 255).astype(np.uint8)
            ).astype(np.float32)
            / 255
        )

    @staticmethod
    def __subtract(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Subtract.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return b - a  # type: ignore

    @staticmethod
    def __divide(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Divide.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return b / np.maximum(0.0001, a)

    @staticmethod
    def __exclusion(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Exclusion.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return a * (1 - b) + b * (1 - a)

    @staticmethod
    def __soft_light(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Blending mode: Soft Light.

        Args:
            a (np.ndarray): The first input image.
            b (np.ndarray): The second input image.

        Returns:
            np.ndarray: The blended image.
        """
        return 2 * b * a + b * b * (1 - 2 * a)
