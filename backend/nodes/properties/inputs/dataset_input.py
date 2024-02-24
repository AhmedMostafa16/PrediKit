from ...properties import expression
from ...properties.inputs.base_input import BaseInput


class DatasetInput(BaseInput):
    """Input a dataset of pandas DataFrame"""

    def __init__(
        self,
        label: str = "Dataset",
        dataset_type: expression.ExpressionJson = "Dataset",
    ):
        super().__init__(dataset_type, label)
