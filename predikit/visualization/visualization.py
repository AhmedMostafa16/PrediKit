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

from ._base import (
    BaseVisualization,
    VisualizationStrategies,
)

pd.options.plotting.backend = "plotly"


class Visualization(BaseVisualization):
    """
    A class that unifies various visualizations.

    Parameters:
        strategy (str): The visualization strategy to use. Available options are:
            - "Bar"
            - "Scatter"
            - "Hist"
            - "CountPlot"
            - "HeatMap"
            - "PairPlot"
            - "BoxPlot"
            - "LinePlot"
            - "PieChart"
            - "AreaPlot"
            - "Hexbin"
            - "Barh"
            - "KDE"
        params (dict): A dictionary of parameters for the visualization. Each parameter
            should be a key-value pair, where the key is a string and the value can be
            a string, integer, or float.

    Attributes:
        _VISUALIZATIONS (dict): A dictionary mapping visualization strategies to their
            corresponding functions.

    Methods:
        barh(df: pd.DataFrame, *args, **kwargs) -> None:
            Returns a BarH plot for a Pandas DataFrame.

        get_traces() -> List[dict]:
            Get the traces or data from the visualization.

        send_json() -> str:
            Convert the visualization to JSON.

        show() -> None:
            Shows the plot.
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

    def __init__(
        self,
        strategy: VisualizationStrategies,
        params: dict[str, str | int | float] = None,
    ) -> None:
        """
        Initialize a Visualization object.

        Args:
            strategy (VisualizationStrategies): The visualization strategy to use.
            params (dict, optional): A dictionary of parameters for the visualization.
                Defaults to None.
        """
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

    def send_json(self) -> str:
        """
        Convert the visualization to JSON.

        Returns:
            str: The visualization data in JSON format.
        """
        return to_json(self.vis)

    def show(self) -> None:
        """
        Shows the plot.
        """
        self.vis.show()


class Subplots(BaseVisualization):
    """
    A class that creates subplots.

    Parameters:
    -----------
    figures : list
        A list of figures to be displayed.
    rows : int
        The number of rows in the subplot.
    cols : int
        The number of columns in the subplot.
    """

    def __init__(self, figures: list, rows: int, cols: int) -> None:
        self.figures = figures
        self.rows = rows
        self.cols = cols

    def subplots(self):
        """
        Creates subplots with axis labels and titles.

        Returns:
            A Plotly figure object with subplots, axis labels, and titles.
        """
        # Create a subplot with the specified number of rows and columns
        this_figure = sp.make_subplots(rows=self.rows, cols=self.cols)

        # Loop through each figure and add its traces to the appropriate subplot
        for i, fig in enumerate(self.figures, 1):  # Start index from 1
            # Get the actual Plotly figure from the Visualization object
            plotly_fig = fig.vis if isinstance(fig, Visualization) else fig
            for trace in fig.get_traces():
                # Calculate row and col indices based on total number of subplots
                row_index = (i - 1) // self.cols + 1
                col_index = (i - 1) % self.cols + 1
                this_figure.add_trace(trace, row=row_index, col=col_index)

                # Extract the title from the figure
                title = (
                    plotly_fig.layout.title.text
                    if plotly_fig.layout.title.text
                    else ""
                )

                # Add title annotation to each subplot
                this_figure.add_annotation(
                    xref="x domain",
                    yref="y domain",
                    x=0.5,
                    y=1.15,
                    showarrow=False,
                    text=title,
                    row=row_index,
                    col=col_index,
                )

        # Add axis labels to each subplot
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                if index < len(self.figures):
                    # Get the actual Plotly figure from the Visualization object
                    plotly_fig = (
                        self.figures[index].vis
                        if isinstance(self.figures[index], Visualization)
                        else self.figures[index]
                    )
                    # Extract labels from the individual figures
                    x_label = plotly_fig.layout.xaxis.title.text
                    y_label = plotly_fig.layout.yaxis.title.text

                    # Update the subplot with the extracted labels
                    this_figure.update_xaxes(
                        title_text=x_label, row=i + 1, col=j + 1
                    )
                    this_figure.update_yaxes(
                        title_text=y_label, row=i + 1, col=j + 1
                    )

        # Adjust layout to avoid overlapping of labels with plots
        this_figure.update_layout(
            autosize=True,
            margin=dict(l=50, r=50, t=50, b=50),
        )

        return this_figure

    def send_json(self, figure):
        """
        Convert the visualization to JSON.

        Parameters:
        -----------
        figure : Plotly figure
            The figure to be converted to JSON.

        Returns:
        --------
        str
            The JSON representation of the figure.
        """
        return to_json(figure)

    def show(self, figure):
        """
        Shows the plot.

        Parameters:
        -----------
        figure : Plotly figure
            The figure to be displayed.
        """
        offline.iplot(figure)
