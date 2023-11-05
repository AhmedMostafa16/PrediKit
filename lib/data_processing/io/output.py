from io import BytesIO
from typing import TypeAlias

from utils.file_utils import FileUtils

Extension: TypeAlias = FileUtils.Extension


def export_file_as(file: BytesIO, ext: Extension) -> None:
    ...
