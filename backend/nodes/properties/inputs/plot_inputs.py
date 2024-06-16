from ...properties.inputs.base_input import BaseInput


class PlotInput(BaseInput):
    """Input a plot"""

    def __init__(
        self,
        label: str = "Plot",
    ):
        super().__init__("Plot", label)

    def enforce(self, value):
        return value

    def toDict(self):
        return {
            **super().toDict(),
            "inputType": "plot",
        }
