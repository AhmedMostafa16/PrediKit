from __future__ import annotations
from .base_output import BaseOutput, OutputKind
from .. import expression


class FileOutput(BaseOutput):
    """Output for saving a local file"""

    def __init__(
        self,
        file_type: expression.ExpressionJson,
        label: str,
        kind: OutputKind = "generic",
    ):
        super().__init__(file_type, label, kind=kind)

    def get_broadcast_data(self, value: str):
        return value


def DatasetFileOutput() -> FileOutput:
    """Output for saving a local dataset file"""
    return FileOutput("DatasetFile", "Dataset File")

