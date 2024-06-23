from .. import expression
from .base_output import (
    BaseOutput,
    OutputKind,
)


class PlotOutput(BaseOutput):
    def __init__(
        self,
        label: str = "Plot",
        plot_type: expression.ExpressionJson = "Plot",
        kind: OutputKind = "plot",
    ):
        super().__init__(
            output_type=expression.intersect(plot_type, "Plot"),
            label=label,
            kind=kind,
            has_handle=False,
        )

    def get_broadcast_data(self, value) -> str:
        return value
