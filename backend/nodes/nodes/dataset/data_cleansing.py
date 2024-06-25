# ruff: noqa: E402
from __future__ import annotations

import os
import sys

import pandas

root = os.path.dirname(os.path.abspath("../../../../predikit/"))
sys.path.append(root)

from typing import cast

from predikit import (
    DataFilteringProcessor,
    FeatureSelection,
    OutliersProcessor,
    RowIdentifier,
    RowSelector,
    RowSorter,
    StringOperationsProcessor,
)
from predikit._typing import FeatureType

from . import category as DatasetCategory
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs.dataset_input import DatasetInput
from ...properties.inputs.generic_inputs import (
    BoolInput,
    DropDownInput,
    TextInput,
)
from ...properties.inputs.numeric_inputs import NumberInput
from ...properties.outputs.dataset_output import DatasetOutput


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
                precision=5,
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
        self.sub = "Data Cleansing"

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
        self.sub = "Data Cleansing"

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


@NodeFactory.register("predikit:dataset:data_filter")
class DataFilterNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Filter a dataset based on a condition."
        self.inputs = [
            DatasetInput(),
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
        self.name = "Data Filter"
        self.icon = "MdFilterAlt"  # ImFilter for advanced filter
        self.sub = "Data Cleansing"

    def run(
        self, dataset: pandas.DataFrame, column, operator: str, value: str
    ) -> pandas.DataFrame:
        try:
            filter = DataFilteringProcessor(
                operator=operator,
                value=value,
            )

            return filter.fit_transform(dataset, column)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")


@NodeFactory.register("predikit:dataset:feature_selection")
class FeatureSelectionNode(NodeBase):
    _options: list[dict[str, str]] = [
        {
            "option": "Number",
            "value": "number",
            "type": "string",
        },
        {
            "option": "String",
            "value": "object",
            "type": "string",
        },
        {
            "option": "Integer",
            "value": "int",
            "type": "string",
        },
        {
            "option": "Float",
            "value": "float",
            "type": "string",
        },
        {
            "option": "Boolean",
            "value": "bool",
            "type": "string",
        },
        {
            "option": "Category",
            "value": "category",
            "type": "string",
        },
        {
            "option": "Object",
            "value": "object",
            "type": "string",
        },
        {
            "option": "Datetime",
            "value": "datetime",
            "type": "string",
        },
        {
            "option": "Timedelta",
            "value": "timedelta",
            "type": "string",
        },
    ]

    def __init__(self):
        super().__init__()
        self.description = "Select features from a dataset."
        # of FeatureType

        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="Include Data Types",
                options=self._options,
                input_type="string",
            ),
            DropDownInput(
                label="Exclude Data Types",
                options=self._options,
                input_type="string",
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]

        self.category = DatasetCategory
        self.name = "Feature Selection"
        self.icon = "TbAtom"
        self.sub = "Feature Engineering"

    def run(
        self,
        dataset: pandas.DataFrame,
        include_dtypes: str,
        exclude_dtypes: str,
    ) -> pandas.DataFrame:
        include_dtypes = cast(FeatureType, include_dtypes)
        exclude_dtypes = cast(FeatureType, exclude_dtypes)

        feature_selection = FeatureSelection(
            include_dtypes=[include_dtypes],
            exclude_dtypes=[exclude_dtypes],
        )

        try:
            return feature_selection.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")


@NodeFactory.register("predikit:dataset:row_selector")
class RowSelectorNode(NodeBase):
    _options_delimiter: dict[str, str] = {
        "Comma": ",",
        "Semicolon": ";",
        "New Line": "\n",
        "Slash": "/",
        "Back Slash": "\\",
    }

    def __init__(self):
        super().__init__()
        self.description = "Select rows from a dataset based on a condition. Press info for more special syntax details."
        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="Delimiter",
                options=[
                    {
                        "option": key,
                        "value": value,
                        "type": "string",
                    }
                    for key, value in self._options_delimiter.items()
                ],
                input_type="string",
            ),
            TextInput(
                label="Condition",
                allow_numbers=True,
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]

        self.category = DatasetCategory
        self.name = "Row Selector"
        self.icon = "TbLayersSelected"
        self.sub = "Row Operations"

    def run(
        self,
        dataset,
        delimiter,
        condition: str,
    ) -> pandas.DataFrame:
        row_selector = RowSelector(
            input=condition,
            delimiter=delimiter,
        )

        try:
            return row_selector.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")


@NodeFactory.register("predikit:dataset:row_identifier")
class RowIdentifierNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Select rows from a dataset based on a condition. Press info for more special syntax details."
        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="New Column Position",
                options=[
                    {
                        "option": "First",
                        "value": "first",
                        "type": "string",
                    },
                    {
                        "option": "Last",
                        "value": "last",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            TextInput(
                label="New Column Name",
                allow_numbers=True,
            ),
            TextInput(
                label="Prefix",
                allow_numbers=True,
            ).make_optional(),
            NumberInput(
                label="Start Value",
                default=1,
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]
        self.category = DatasetCategory
        self.name = "Row Identifier"
        self.icon = "MdPermIdentity"
        self.sub = "Row Operations"

    def run(
        self,
        dataset,
        new_column_name,
        value_prefix,
        start_value,
        position,
    ) -> pandas.DataFrame:
        row_identifier = RowIdentifier(
            new_col_name=new_column_name,
            value_prefix=value_prefix,
            start_value=start_value,
            position=position,
        )

        try:
            return row_identifier.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")


@NodeFactory.register("predikit:dataset:row_sorter")
class RowSorterNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Sort rows in a dataset based on a column."
        self.inputs = [
            DatasetInput(),
            TextInput(
                label="Column",
                allow_numbers=True,
            ),
            BoolInput(
                label="Ascending",
            ),
            DropDownInput(
                label="Sort Method",
                options=[
                    {
                        "option": "Quick Sort",
                        "value": "quicksort",
                        "type": "string",
                    },
                    {
                        "option": "Merge Sort",
                        "value": "mergesort",
                        "type": "string",
                    },
                    {
                        "option": "Heap Sort",
                        "value": "heapsort",
                        "type": "string",
                    },
                    {
                        "option": "Stable",
                        "value": "stable",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            DropDownInput(
                label="Empty Data Position",
                options=[
                    {
                        "option": "First",
                        "value": "first",
                        "type": "string",
                    },
                    {
                        "option": "Last",
                        "value": "last",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
        ]
        self.outputs = [
            DatasetOutput(label="Dataset"),
        ]
        self.category = DatasetCategory
        self.name = "Row Sorter"
        self.icon = "MdSortByAlpha"
        self.sub = "Row Operations"

    def run(
        self, dataset, column, ascending, kind, na_position
    ) -> pandas.DataFrame:
        row_sorter = RowSorter(
            column,
            ascending,
            kind,
            na_position,
        )

        try:
            return row_sorter.fit_transform(dataset)
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
