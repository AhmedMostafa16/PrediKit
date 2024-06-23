from abc import ABC
from enum import StrEnum
from typing import Any


class BaseVisualization(ABC):
    """Base class for all visualizations."""

    def send_json() -> Any:
        pass

    def show() -> Any:
        pass

    def subplots() -> Any:
        pass

    def get_traces() -> list[dict]:
        pass


class VisualizationStrategies(StrEnum):
    Bar = "bar"
    Scatter = "scatter"
    Hist = "histogram"
    Box = "box"
    Line = "line"
    """
    CountPlot = 'countplot'
    HeatMap = 'heatmap'
    PairPlot = 'pairplot'
    LinePlot = 'lineplot'
    BoxPlot = 'boxplot'
    PairPlot = 'pairplot'
    """

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
            case "box" | "bosplot":
                return cls.Box
            case "line" | "lineplot":
                return cls.Line
            case _:
                raise ValueError(f"Invalid visualization strategy: {strategy}")


"""
            case "countplot" | "count":
                return cls.CountPlot
            case "heatmap":
                return cls.HeatMap
            case "boxplot" | "box":
                return cls.BoxPlot
            case "lineplot" | "line":
                return cls.LinePlot
            case "pairplot" | "pair":
                return cls.PairPlot
            """
