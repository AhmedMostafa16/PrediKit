import pandas
from ...properties import expression
from ...properties.inputs.base_input import BaseInput


class DatasetInput(BaseInput):
    """Input a dataset of pandas DataFrame"""

    def __init__(
        self,
        label: str = "Dataset",
    ):
        super().__init__("Dataset", label)

    def enforce(self, value):
        # assert isinstance(value, pandas.DataFrame)
        return value

    def toDict(self):
        return {
            **super().toDict(),
            "inputType": "dataset",
        }
