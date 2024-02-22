from __future__ import annotations
from .base_output import BaseOutput


class FileOutput(BaseOutput):
    """Output for saving a local file"""

    def __init__(self, file_type: str, label: str):
        super().__init__(f"file::{file_type}", label)


def DatasetFileOutput() -> FileOutput:
    """Output for saving a local dataset file"""
    return FileOutput("DatasetFile", "Dataset File")
