import logging

from pandas import DataFrame

from predikit._typing import DfExporter
from predikit.utils.io_utils import (
    FileExtension,
    abs_path,
    append_to_home,
    ext_to_str,
    get_home,
    init_dir,
)


class DataFrameExporter:
    _EXPORTERS: dict[FileExtension, DfExporter] = {
        FileExtension.CSV: DataFrame.to_csv,
        FileExtension.JSON: DataFrame.to_json,
        FileExtension.PARQUET: DataFrame.to_parquet,
        FileExtension.EXCEL: DataFrame.to_excel,
        FileExtension.PICKLE: DataFrame.to_pickle,
    }

    def __init__(
        self,
        df: DataFrame,
        *,
        extension: FileExtension,
        filename: str = "out",
        **params,
    ) -> None:
        self._df = df
        self._extension = extension
        self._filename = filename
        self._params = params

    @property
    def default_dir(self):
        DIR = "predikit_out"
        return append_to_home(DIR)

    @property
    def default_path(self):
        file = self._filename + ext_to_str(self._extension)
        return abs_path(self.default_dir, file)

    def export(self) -> None:
        init_dir(self.default_dir)
        logging.info(f"Exporting to {self.default_path} ...")
        self._get_exporter(self._extension)(
            self._df, self.default_path, **self._params
        )

    def _get_exporter(self, ext: FileExtension) -> DfExporter:
        exporter = self._EXPORTERS.get(ext)
        if not exporter:
            raise TypeError("No exporter for type {ext}")
        return exporter
