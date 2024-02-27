from typing import Dict, List, Union
import numpy as np
import pandas

from .. import expression

from .base_input import BaseInput


class DropDownInput(BaseInput):
    """Input for a dropdown"""

    def __init__(
        self,
        input_type: expression.ExpressionJson,
        label: str,
        options: List[Dict],
    ):
        super().__init__(input_type, label, kind="dropdown", has_handle=False)
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
        min_length: int = 1,
        max_length: Union[int, None] = None,
        placeholder: Union[str, None] = None,
        allow_numbers: bool = True,
    ):
        super().__init__(
            ["string", "number"] if allow_numbers else "string",
            label,
            has_handle=has_handle,
            kind="text-line",
        )
        self.min_length = min_length
        self.max_length = max_length
        self.placeholder = placeholder

    def enforce(self, value) -> str:
        if isinstance(value, float) and int(value) == value:
            # stringify integers values
            return str(int(value))
        return str(value)

    def toDict(self):
        return {
            **super().toDict(),
            "minLength": self.min_length,
            "maxLength": self.max_length,
            "placeholder": self.placeholder,
        }


class BoolInput(DropDownInput):
    """Input for a checkbox"""

    def __init__(self, label: str):
        super().__init__(
            input_type="bool",
            label=label,
            options=[
                {
                    "option": "True",
                    "value": int(True),  # 1
                    "type": "true",
                },
                {
                    "option": "False",
                    "value": int(False),  # 0
                    "type": "false",
                },
            ],
        )
        self.associated_type = bool

    def enforce(self, value: object) -> bool:
        value = super().enforce(value)
        return bool(value)


class NoteTextAreaInput(BaseInput):
    """Input for note text"""

    def __init__(self, label: str = "Note Text"):
        super().__init__("string", label, has_handle=False, kind="text")
        self.resizable = True

    def toDict(self):
        return {
            **super().toDict(),
            "resizable": self.resizable,
        }


class AnyInput(BaseInput):
    def __init__(self, label: str):
        super().__init__(input_type="any", label=label)

    def enforce_(self, value):
        # The behavior for optional inputs and None makes sense for all inputs except this one.
        return value


class ClipboardInput(BaseInput):
    """Input for pasting from clipboard"""

    def __init__(self, label: str = "Clipboard input"):
        super().__init__(
            ["Dataset", "string", "number"], label, kind="text-line"
        )
        self.input_conversion = """
            match Input {
                Dataset => "<Dataset>",
                _ as i => i,
            }
        """

    def enforce(self, value):
        if isinstance(value, pandas.DataFrame):
            return value.to_csv(index=False)

        if isinstance(value, float) and int(value) == value:
            # stringify integers values
            return str(int(value))

        return str(value)


def MathOpsDropdown() -> DropDownInput:
    """Input for selecting math operation type from dropdown"""
    return DropDownInput(
        input_type="MathOperation",
        label="Math Operation",
        options=[
            {
                "option": "Add (+)",
                "value": "add",
                "type": """MathOperation { operation: "add" }""",
            },
            {
                "option": "Subtract (-)",
                "value": "sub",
                "type": """MathOperation { operation: "sub" }""",
            },
            {
                "option": "Multiply (×)",
                "value": "mul",
                "type": """MathOperation { operation: "mul" }""",
            },
            {
                "option": "Divide (÷)",
                "value": "div",
                "type": """MathOperation { operation: "div" }""",
            },
            {
                "option": "Exponent/Power (^)",
                "value": "pow",
                "type": """MathOperation { operation: "pow" }""",
            },
            {
                "option": "Maximum",
                "value": "max",
                "type": """MathOperation { operation: "max" }""",
            },
            {
                "option": "Minimum",
                "value": "min",
                "type": """MathOperation { operation: "min" }""",
            },
            {
                "option": "Modulo",
                "value": "mod",
                "type": """MathOperation { operation: "mod" }""",
            },
        ],
    )


def LogicalOpsDropdown() -> DropDownInput:
    """Input for selecting logical operation type from dropdown"""
    return DropDownInput(
        input_type="LogicalOperation",
        label="Logical Operation",
        options=[
            {
                "option": "Greater Than (>)",
                "value": "gt",
                "type": """LogicalOperation { operation: "gt" }""",
            },
            {
                "option": "Greater Than or Equal (≥)",
                "value": "ge",
                "type": """LogicalOperation { operation: "ge" }""",
            },
            {
                "option": "Less Than (<)",
                "value": "lt",
                "type": """LogicalOperation { operation: "lt" }""",
            },
            {
                "option": "Less Than or Equal (≤)",
                "value": "le",
                "type": """LogicalOperation { operation: "le" }""",
            },
            {
                "option": "Equal (==)",
                "value": "eq",
                "type": """LogicalOperation { operation: "eq" }""",
            },
            {
                "option": "Not Equal (!=)",
                "value": "ne",
                "type": """LogicalOperation { operation: "ne" }""",
            },
        ],
    )


def IteratorInput():
    """Input for showing that an iterator automatically handles the input"""
    return BaseInput("IteratorAuto", "Auto (Iterator)", has_handle=False)
