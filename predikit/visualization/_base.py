from abc import (
    ABC,
    abstractmethod
)

from enum import StrEnum

from matplotlib.pyplot import (
    scatter,
    hist,
    bar,
)

from seaborn import (
    countplot,
    heatmap,
    pairplot,
)

from sklearn.base import (
    ClassifierMixin,
    BaseEstimator
)

from numpy import ndarray
from .._typing import MatrixLike, Any


class BaseVisualization(ABC):
    """Base class for all visualizations."""

    def plot() -> Any:
        pass


class VisualizationStrategies(StrEnum):
    Bar = 'bar'
    Scatter = 'scatter'
    Hist = 'hist'
    CountPlot = 'countplot'
    HeatMap = 'heatmap'
    PairPlot = 'pairplot'

    @classmethod
    def from_str(cls, strategy: str) -> "VisualizationStrategies":
        """
        Returns the enumeration member corresponding to the given string.

        Parameters
        ----------
        strategy : str
            The string representation of the strategy.

        Returns
        -------
        VisualizationStrategies
            The enumeration member corresponding to the given string.
        """
        strategy = strategy.lower()
        match strategy:
            case "bar" | "barplot":
                return cls.Bar
            case "scatter" | "scatterplot":
                return cls.Scatter
            case "hist" | "histogram":
                return cls.Hist
            case "countplot" | "count":
                return cls.CountPlot
            case "heatmap":
                return cls.HeatMap
            case _:
                raise ValueError(f"Invalid visualization strategy: {strategy}")
