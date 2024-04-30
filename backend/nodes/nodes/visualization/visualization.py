import os
from re import T
import sys
from typing import Literal

import pandas
import plotly.io as pio

pandas.options.plotting.backend = "plotly"

from ...properties.outputs.plot_output import PlotOutput
from ...properties.inputs.generic_inputs import (
    DropDownInput,
    TextInput,
)
from ...properties.inputs.dataset_input import DatasetInput
from ...node_base import NodeBase
from ...node_factory import NodeFactory
from . import category as VisualizationsCategory


@NodeFactory.register("predikit:visualization:visualize")
class VisualizationNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Visualize a dataset using a plot."
        self.inputs = [
            DatasetInput(),
            DropDownInput(
                label="Plot Type",
                options=[
                    {
                        "option": "Line",
                        "value": "line",
                        "type": "string",
                    },
                    {
                        "option": "Bar",
                        "value": "bar",
                        "type": "string",
                    },
                    {
                        "option": "Scatter",
                        "value": "scatter",
                        "type": "string",
                    },
                    {
                        "option": "Pie",
                        "value": "pie",
                        "type": "string",
                    },
                    {
                        "option": "Histogram",
                        "value": "histogram",
                        "type": "string",
                    },
                    {
                        "option": "Box",
                        "value": "box",
                        "type": "string",
                    },
                    {
                        "option": "Kernel Dense Estimation (KDE)",
                        "value": "kde",
                        "type": "string",
                    },
                    {
                        "option": "Density",
                        "value": "density",
                        "type": "string",
                    },
                    {
                        "option": "Area",
                        "value": "area",
                        "type": "string",
                    },
                    {
                        "option": "Hexbin",
                        "value": "hexbin",
                        "type": "string",
                    },
                ],
                input_type="string",
            ),
            TextInput(
                label="Title",
                allow_numbers=True,
                has_handle=True,
            ),
            TextInput(
                label="X-axis",
                allow_numbers=True,
                has_handle=True,
                placeholder="X-axis Column Name",
            ),
            TextInput(
                label="Y-axis",
                allow_numbers=True,
                has_handle=True,
                placeholder="Y-axis Column Name",
            ),
        ]
        self.outputs = [PlotOutput()]
        self.category = VisualizationsCategory
        self.name = "Visualize"
        self.icon = "MdOutlineAutoGraph"
        self.sub = "Plotting"
        self.side_effects = True

    def run(
        self,
        dataset: pandas.DataFrame,
        plot_type: Literal[
            "line",
            "bar",
            "barh",
            "hist",
            "box",
            "kde",
            "density",
            "area",
            "pie",
            "scatter",
            "hexbin",
        ],
        title: str,
        x_axis: str,
        y_axis: str,
    ):
        try:
            fig = dataset.plot(
                kind=plot_type,
                title=title,
                x=x_axis,
                y=y_axis,
            )
            return pio.to_json(fig, pretty=True)

        except Exception as e:
            raise Exception(f"Failed to visualize dataset: {str(e)}")
