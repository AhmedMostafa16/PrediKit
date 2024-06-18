from __future__ import annotations

import math
from typing import Union

from . import category as UtilityCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import (
    MathOpsDropdown,
    NumberInput,
)
from ...properties.outputs import NumberOutput


@NodeFactory.register("predikit:utility:math")
class MathNode(NodeBase):
    special_mod_numbers = (0.0, float("inf"), float("-inf"), float("nan"))

    def __init__(self):
        super().__init__()
        self.description = "Perform mathematical operations on numbers."
        self.inputs = [
            NumberInput(
                "First Operand",
                minimum=None,
                maximum=None,
                precision=100,
                controls_step=1,
            ),
            MathOpsDropdown(),
            NumberInput(
                "Second Operand",
                minimum=None,
                maximum=None,
                precision=100,
                controls_step=1,
            ),
        ]
        self.outputs = [
            NumberOutput(
                "Result",
                output_type="""
                match Input1.operation {
                    "add" => Input0 + Input2,
                    "sub" => Input0 - Input2,
                    "mul" => Input0 * Input2,
                    "div" => Input0 / Input2,
                    "pow" => pow(Input0, Input2),
                    "max" => max(Input0, Input2),
                    "min" => min(Input0, Input2),
                    "mod" => mod(Input0, Input2),
                    _ => number
                }
                """,
            )
        ]

        self.category = UtilityCategory
        self.name = "Math"
        self.icon = "MdCalculate"
        self.sub = "Math"

    def run(
        self, in1: Union[int, float], op: str, in2: Union[int, float]
    ) -> Union[int, float]:
        if op == "add":
            return in1 + in2
        if op == "sub":
            return in1 - in2
        if op == "mul":
            return in1 * in2
        if op == "div":
            return in1 / in2
        if op == "pow":
            return in1**in2
        if op == "max":
            return max(in1, in2)
        if op == "min":
            return min(in1, in2)
        if op == "mod":
            if (
                in1 in MathNode.special_mod_numbers
                or in2 in MathNode.special_mod_numbers
            ):
                return in1 - in2 * math.floor(in1 / in2)
            return in1 % in2
        else:
            raise RuntimeError(f"Unknown operator {op}")
