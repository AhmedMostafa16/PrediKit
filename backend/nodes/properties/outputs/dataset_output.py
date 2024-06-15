from nodes.utils.dataset_utils import get_dataframe_fields
import pandas

from ...properties import expression
from ...properties.outputs.base_output import (
    BaseOutput,
    OutputKind,
)


class DatasetOutput(BaseOutput):
    """Output a dataset of pandas DataFrame"""

    def __init__(
        self,
        label: str = "Dataset",
        dataset_type: expression.ExpressionJson = "Dataset",
        kind: OutputKind = "dataset",
        has_handle: bool = True,
        broadcast_type: bool = False,
    ):
        super().__init__(
            expression.intersect(dataset_type, "Dataset"),
            label,
            kind=kind,
            has_handle=has_handle,
        )
        self.broadcast_type = broadcast_type

    def get_broadcast_data(self, value: pandas.DataFrame):
        if not self.broadcast_type:
            return None

        df: pandas.DataFrame = value

        columns, data, dfindex, dtype, shape = get_dataframe_fields(df)

        return {
            "columns": columns,
            "data": data,
            "index": dfindex,
            "dtype": dtype,
            "shape": shape,
        }
