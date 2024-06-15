from ._base import (
    BaseVisualization,
    VisualizationStrategies,
)
from .._typing import (
    Any,
    MatrixLike,
)

import pandas as pd
from plotly import offline
from plotly.express import (
    area,
    bar,
    box,
    density_heatmap,
    histogram,
    line,
    pie,
    scatter,
)
from plotly.figure_factory import create_distplot
from plotly.graph_objs import Figure
from plotly.io import to_json
import plotly.subplots as sp

pd.options.plotting.backend = "plotly"

class Visualization(BaseVisualization):
    """
    A class that unifies various visualizations.

    ### Parameters
    strategy : {"Bar", "Scatter", "Hist", "CountPlot", "HeatMap",
    "PairPlot", "BoxPlot", "LinePlot", "PieChart" , "AreaPlot", "Hexbin", "Barh", "KDE"},
    default= None

    params: a dictionary of parameters
    {'parameter': value -> (str, int or float)}.
    """

    @staticmethod
    def barh(df: pd.DataFrame, *args, **kwargs):
        """Returns BarH plot for a Pandas dataframe"""
        return df.plot.barh(*args, **kwargs)

    _VISUALIZATIONS: dict = {
        VisualizationStrategies.Bar: bar,
        VisualizationStrategies.Scatter: scatter,
        VisualizationStrategies.Hist: histogram,
        VisualizationStrategies.Box: box,
        VisualizationStrategies.Line: line,
        VisualizationStrategies.Pie: pie,
        VisualizationStrategies.Area: area,
        VisualizationStrategies.HeatMap: density_heatmap,
        VisualizationStrategies.KDE: create_distplot,
        VisualizationStrategies.BarH: barh,
    }
    """
        VisualizationStrategies.CountPlot: countplot,
        VisualizationStrategies.PairPlot: pairplot,
        """

    def __init__(
        self,
        strategy: VisualizationStrategies,
        params: dict[str, str | int | float] = None,
    ) -> None:
        if params is None:
            params = {}
        if strategy is None:
            raise ValueError("Select a visualization.")
        else:
            self.strategy = VisualizationStrategies.from_str(strategy)

        if params is None or not isinstance(params, dict) or len(params) == 0:
            self.vis = self._VISUALIZATIONS[self.strategy]()
        else:
            self.vis = self._VISUALIZATIONS[self.strategy](**params)

    def get_traces(self) -> list[dict]:
        """
        Get the traces or data from the visualization.

        Returns:
            List of dictionaries representing the traces.
        """
        if isinstance(self.vis, Figure):
            return self.vis.data
        else:
            raise TypeError(
                "Visualization object does not contain valid data."
            )

    def send_json(self):
        """
        Convert the visualization to JSON.

        Args:
            .
        """
        return to_json(self.vis)

    def show(self):
        """
        Shows the plot.
        """
        self.vis.show()


class Subplots(BaseVisualization):
    """
    A class that creates subplots.

    ### Parameters
    figures: list
        A list of figures to be displayed.
    rows: int
        The number of rows in the subplot.
    cols: int
        The number of columns in the subplot.
    """

    def __init__(self, figures: list, rows: int, cols: int) -> None:
        self.figures = figures
        self.rows = rows
        self.cols = cols

    def subplots(self):
        """
        Creates subplots.
        """
        # Create a subplot with the specified number of rows and columns
        this_figure = sp.make_subplots(rows=self.rows, cols=self.cols)

        # Loop through each figure and add its traces to the appropriate subplot
        for i, fig in enumerate(self.figures, 1):  # Start index from 1
            for trace in fig.get_traces():
                # Calculate row and col indices based on total number of subplots
                row_index = (i - 1) // self.cols + 1
                col_index = (i - 1) % self.cols + 1
                this_figure.add_trace(trace, row=row_index, col=col_index)

        return this_figure

    def send_json(self, figure):
        """
        Convert the visualization to JSON.

        Args:
            .
        """
        return to_json(figure)

    def show(self, figure):
        """
        Shows the plot.

        Args:
            figure: The figure to be displayed.
        """
        offline.iplot(figure)
