from typing import Dict, List, Union

from .base_input import BaseInput


class DropDownInput(BaseInput):
    """Input for a dropdown"""

    def __init__(
        self,
        label: str,
        options: List[Dict],
        input_type: str = "generic",
    ):
        super().__init__(f"dropdown::{input_type}", label, has_handle=False)
        self.options = options

    def toDict(self):
        return {
            **super().toDict(),
            "options": self.options,
        }

    def make_optional(self):
        raise ValueError("DropDownInput cannot be made optional")

    def enforce(self, value):
        accepted_values = [o["value"] for o in self.options]
        assert value in accepted_values, f"{value} is not a valid option"
        return value


class TextInput(BaseInput):
    """Input for arbitrary text"""

    def __init__(
        self,
        label: str,
        has_handle=True,
        max_length: Union[int, None] = None,
    ):
        super().__init__(f"text::any", label, has_handle=has_handle)
        self.max_length = max_length

    def toDict(self):
        return {
            **super().toDict(),
            "maxLength": self.max_length,
        }


class NoteTextAreaInput(BaseInput):
    """Input for note text"""

    def __init__(self, label: str = "Note Text"):
        super().__init__(f"textarea::note", label, has_handle=False)
        self.resizable = True

    def toDict(self):
        return {
            **super().toDict(),
            "resizable": self.resizable,
        }


def MathOpsDropdown() -> DropDownInput:
    """Input for selecting math operation type from dropdown"""
    return DropDownInput(
        "Math Operation",
        [
            {
                "option": "Add (+)",
                "value": "add",
            },
            {
                "option": "Subtract (-)",
                "value": "sub",
            },
            {
                "option": "Multiply (×)",
                "value": "mul",
            },
            {
                "option": "Divide (÷)",
                "value": "div",
            },
            {
                "option": "Exponent/Power (^)",
                "value": "pow",
            },
            {
                "option": "Maximum",
                "value": "max",
            },
            {
                "option": "Minimum",
                "value": "min",
            },
        ],
        input_type="math-operations",
    )


def StackOrientationDropdown() -> DropDownInput:
    """Input for selecting stack orientation from dropdown"""
    return DropDownInput(
        "Orientation",
        [
            {
                "option": "Horizontal",
                "value": "horizontal",
            },
            {
                "option": "Vertical",
                "value": "vertical",
            },
        ],
    )


def IteratorInput():
    """Input for showing that an iterator automatically handles the input"""
    return BaseInput("iterator::auto", "Auto (Iterator)", has_handle=False)
