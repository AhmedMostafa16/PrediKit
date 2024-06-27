from abc import ABC
from enum import StrEnum
from typing import Any


class BaseVisualization(ABC):
    """Base class for all visualizations."""

    def send_json(self) -> Any:
        """Send the visualization data as JSON."""
        raise NotImplementedError()

    def show(self) -> Any:
        """Display the visualization."""
        raise NotImplementedError()

    def subplots(self) -> Any:
        """Create subplots for the visualization."""
        raise NotImplementedError()

    def get_traces(self) -> list[dict]:
        """Get the traces for the visualization."""
        raise NotImplementedError()


class VisualizationStrategies(StrEnum):
    """
    Enumeration class representing different visualization strategies.

    Attributes
    ----------
    Bar : str
        Bar chart strategy.
    Scatter : str
        Scatter plot strategy.
    Hist : str
        Histogram strategy.
    Box : str
        Box plot strategy.
    Line : str
        Line plot strategy.
    Pie : str
        Pie chart strategy.
    Area : str
        Area plot strategy.
    HeatMap : str
        Heatmap strategy.
    KDE : str
        Kernel Density Estimation (KDE) strategy.
    BarH : str
        Horizontal bar chart strategy.
    """

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

        Raises
        ------
        ValueError
            If an invalid visualization strategy is provided.
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
