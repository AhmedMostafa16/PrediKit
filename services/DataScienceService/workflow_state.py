from dataclasses import dataclass
from typing import ClassVar

from predikit import FileExtension


@dataclass(frozen=True)
class WorkflowState:
    original_file_extension: ClassVar[FileExtension | None] = None
