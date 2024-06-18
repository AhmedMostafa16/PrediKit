from abc import ABC
from enum import StrEnum

from .._typing import Any


class BaseVisualization(ABC):
    """Base class for all visualizations."""

    def send_json(self) -> Any:
        raise NotImplementedError()

    def show(self) -> Any:
        raise NotImplementedError()

    def subplots(self) -> Any:
        raise NotImplementedError()

    def get_traces(self) -> list[dict]:
        raise NotImplementedError()


class VisualizationStrategies(StrEnum):
    Bar = "bar"
    Scatter = "scatter"
    Hist = "histogram"
    Box = "box"
    Line = "line"
    Pie = "pie"
    Area = "area"
    HeatMap = "heatmap"
    KDE = "kde"
    BarH = "barh"
    """
    CountPlot = 'countplot'
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
            case "pie" | "pieplot" | "piechart":
                return cls.Pie
            case "area" | "areaplot":
                return cls.Area
            case "heatmap":
                return cls.HeatMap
            case "kde":
                return cls.KDE
            case "barh":
                return cls.BarH
            case _:
                raise ValueError(f"Invalid visualization strategy: {strategy}")


"""
            case "countplot" | "count":
                return cls.CountPlot
            case "pairplot" | "pair":
                return cls.PairPlot
            """
