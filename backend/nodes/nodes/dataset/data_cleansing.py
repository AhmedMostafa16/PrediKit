from __future__ import annotations
import os
import re
import sys

import pandas

from predikit.preprocessing.data_filtering import BasicFilteringProcessor


root = os.path.dirname(os.path.abspath("../../../../predikit/"))
sys.path.append(root)

from predikit import (
    OutliersProcessor,
    StringOperationsProcessor,
)

from ...properties.inputs.dataset_input import DatasetInput
from ...properties.inputs.generic_inputs import (
    BoolInput,
    DropDownInput,
    TextInput,
)
from ...properties.inputs.numeric_inputs import NumberInput
from ...properties.outputs.dataset_output import DatasetOutput

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory


@NodeFactory.register("predikit:dataset:outliers")
class OutliersNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Detect and handle outliers in a dataset."
        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="Detection Method",
                options=[
                    {
                        "option": "Z-Score",
                        "value": "zscore",
                        "type": "string",
                    },
                    {
                        "option": "IQR",
                        "value": "iqr",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            NumberInput(
                label="Threshold",
                default=1.5,
                minimum=0,
                maximum=10,
                precision=3,
                hide_trailing_zeros=True,
                controls_step=0.1,
            ),
            BoolInput(
                "Add Indicator Column",
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]

        self.category = DatasetCategory
        self.name = "Detect Outliers"
        self.icon = "BsCookie"
        self.sub = "Data Cleasing"

    def run(self, dataset, method, threshold, add_indicator_column):
        outliers_processor = OutliersProcessor(
            add_indicator=add_indicator_column,
            method=method,
            threshold=threshold,
        )

        try:
            result = outliers_processor.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

        return result


@NodeFactory.register("predikit:dataset:string_operations")
class StringOperationsNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Perform operations on string columns in a dataset."
        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="Case Modification",
                options=[
                    {
                        "option": "None",
                        "value": "null",
                        "type": "null",
                    },
                    {
                        "option": "Lowercase",
                        "value": "lower",
                        "type": "string",
                    },
                    {
                        "option": "Uppercase",
                        "value": "upper",
                        "type": "string",
                    },
                    {
                        "option": "Title Case",
                        "value": "title",
                        "type": "string",
                    },
                    {
                        "option": "Swap Case",
                        "value": "swap",
                        "type": "string",
                    },
                    {
                        "option": "Capitalize First Letter",
                        "value": "capitalize",
                        "type": "string",
                    },
                    {
                        "option": "Casefold",
                        "value": "casefold",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            BoolInput("Remove Whitespace"),
            BoolInput("Remove Numbers"),
            BoolInput("Remove Letters"),
            BoolInput("Remove Punctuation"),
            BoolInput("Trim"),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]

        self.category = DatasetCategory
        self.name = "String Operations"
        self.icon = "MdOutlineTextFields"
        self.sub = "Data Cleasing"

    def run(
        self,
        dataset,
        case_modifier,
        remove_whitespace,
        remove_numbers,
        remove_punctuation,
        remove_letters,
        trim,
    ):
        string_operations_processor = StringOperationsProcessor(
            case_modifier=case_modifier,
            remove_whitespace=remove_whitespace,
            remove_numbers=remove_numbers,
            remove_punctuation=remove_punctuation,
            remove_letters=remove_letters,
            trim=trim,
        )
        try:
            result = string_operations_processor.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

        return result


@NodeFactory.register("predikit:dataset:basic_filter")
class BasicFilterNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Filter a dataset based on a condition."
        self.inputs = [
            DatasetInput(),
            # DropDownInput(
            #     label="Column",
            #     options=[
            #         {"option": col, "value": col, "type": "string"}
            #         for col in get_column_names_from_node_input(self.inputs[0])
            #     ],
            #     input_type="string",
            # ),
            TextInput(
                label="Column",
                allow_numbers=True,
            ),
            DropDownInput(
                label="Operator",
                options=[
                    {
                        "option": "Equal",
                        "value": "eq",
                        "type": "string",
                    },
                    {
                        "option": "Not Equal",
                        "value": "ne",
                        "type": "string",
                    },
                    {
                        "option": "Greater Than",
                        "value": "gt",
                        "type": "string",
                    },
                    {
                        "option": "Greater Than or Equal",
                        "value": "ge",
                        "type": "string",
                    },
                    {
                        "option": "Less Than",
                        "value": "lt",
                        "type": "string",
                    },
                    {
                        "option": "Less Than or Equal",
                        "value": "le",
                        "type": "string",
                    },
                    {
                        "option": "Is In",
                        "value": "in",
                        "type": "string",
                    },
                    {
                        "option": "Is Not In",
                        "value": "nin",
                        "type": "string",
                    },
                    {
                        "option": "Contains",
                        "value": "contains",
                        "type": "string",
                    },
                    {
                        "option": "Does Not Contain",
                        "value": "does_not_contain",
                        "type": "string",
                    },
                    {
                        "option": "Starts With",
                        "value": "starts_with",
                        "type": "string",
                    },
                    {
                        "option": "Ends With",
                        "value": "ends_with",
                        "type": "string",
                    },
                    {
                        "option": "Is Null",
                        "value": "is_null",
                        "type": "string",
                    },
                    {
                        "option": "Is Not Null",
                        "value": "is_not_null",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            TextInput(
                label="Value",
                allow_numbers=True,
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]

        self.category = DatasetCategory
        self.name = "Basic Filter"
        self.icon = "MdFilterAlt"  # ImFilter for advanced filter
        self.sub = "Data Cleasing"

    def run(
        self, dataset: pandas.DataFrame, column, operator: str, value: str
    ) -> pandas.DataFrame:
        try:
            filter = BasicFilteringProcessor(
                operator=operator,
                value=value,
            )

            return filter.fit_transform(dataset, column)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
