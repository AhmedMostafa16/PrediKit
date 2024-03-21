import matplotlib.pyplot as plt
from matplotlib.pyplot import (
    bar,
    hist,
    scatter,
)
from numpy import (
    log,
    ndarray,
)
from seaborn import (
    countplot,
    heatmap,
    pairplot,
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
    "PairPlot"}, default= None

    params: a dictionary of parameters
    {'parameter': value -> (str, int or float)}.
    """

    _VISUALIZATIONS: dict[VisualizationStrategies, "Visualization"] = {
        VisualizationStrategies.Bar: bar,
        VisualizationStrategies.Scatter: scatter,
        VisualizationStrategies.Hist: hist,
        VisualizationStrategies.CountPlot: countplot,
        VisualizationStrategies.HeatMap: heatmap,
        VisualizationStrategies.PairPlot: pairplot,
    }

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

    def plot(self):
        """
        Plots the data based on the strategy selected.

        Args:
            .
        """
        """
        x_label = ""
        y_label = ""
        plot = self.vis.plot()
        if x_label is not None:
            plot.xlabel(x_label)
        if y_label is not None:
            plot.ylabel(y_label)
        plot.show(plot)
        """
        plot = self.vis.plot()
        return self.vis.plot()
