import matplotlib.pyplot as plt

"""
from matplotlib.pyplot import (
    bar,
    boxplot,
    hist,
    scatter,
)
"""
import numpy as np
from numpy import (
    log,
    ndarray,
)
from pandas import DataFrame

"""
from seaborn import (
    countplot,
    heatmap,
    lineplot,
    pairplot,
)
"""

from plotly.express import (
    bar,
    box,
    histogram,
    line,
    scatter,
)
from plotly.io import to_json
from plotly.graph_objs import(
    Figure,
    Layout,
)

from .._typing import (
    Any,
    MatrixLike,
)
from ._base import (
    BaseVisualization,
    VisualizationStrategies,
)


class Visualization(BaseVisualization):
    """
    A class that unifies various visualizations.

    ### Parameters
    strategy : {"Bar", "Scatter", "Hist", "CountPlot", "HeatMap",
    "PairPlot", "BoxPlot", "LinePlot"}, default= None

    params: a dictionary of parameters
    {'parameter': value -> (str, int or float)}.
    """

    _VISUALIZATIONS: dict[VisualizationStrategies, "Visualization"] = {
        VisualizationStrategies.Bar: bar,
        VisualizationStrategies.Scatter: scatter,
        VisualizationStrategies.Hist: histogram,
        VisualizationStrategies.Box: box,
        VisualizationStrategies.Line: line,
    }
    """
        VisualizationStrategies.CountPlot: countplot,
        VisualizationStrategies.HeatMap: heatmap,
        VisualizationStrategies.PairPlot: pairplot,
        VisualizationStrategies.LinePlot: lineplot,
        VisualizationStrategies.BoxPlot: boxplot,
        """

    def __init__(
        self,
        strategy: VisualizationStrategies = None,
        params: dict[str, str | int | float] = None,
    ) -> None:
        if strategy is None:
            raise ValueError("Select a visualization.")
        else:
            self.strategy = VisualizationStrategies.from_str(strategy)

        if params is None:
            self.vis = self._VISUALIZATIONS[self.strategy]()
        else:
            self.vis = self._VISUALIZATIONS[self.strategy](**params)

    def send_json(self):
        """
        Plots the data based on the strategy selected.

        Args:
            .
        """
        return to_json(self.vis)
    
    def show(self):
        """
        Shows the plot.
        """
        self.vis.show()
