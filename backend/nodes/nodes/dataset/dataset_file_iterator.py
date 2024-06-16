from __future__ import annotations

import os
from typing import Tuple, List

import pandas
from backend.nodes.nodes.dataset.load_dataset import DatasetReadNode
from backend.nodes.properties.outputs.dataset_output import DatasetOutput
from process import IteratorContext
from sanic.log import logger

from . import category as DatasetCategory
from ...node_base import IteratorNodeBase, NodeBase
from ...node_factory import NodeFactory
from ...properties.inputs import IteratorInput, DirectoryInput
from ...properties.outputs import (
    DirectoryOutput,
    TextOutput,
    NumberOutput,
)
from ...utils.dataset_utils import get_available_dataset_formats
from ...utils.utils import numerical_sort

DATASET_ITERATOR_NODE_ID = "predikit:dataset:file_iterator_load"


@NodeFactory.register(DATASET_ITERATOR_NODE_ID)
class DatasetFileIteratorLoadDatasetNode(NodeBase):
    def __init__(self):
        super().__init__()
        self.description = ""
        self.inputs = [IteratorInput().make_optional()]
        self.outputs = [
            DatasetOutput(broadcast_type=True),
            DirectoryOutput("Dataset Directory"),
            TextOutput("Subdirectory Path"),
            TextOutput("Dataset Name"),
            NumberOutput("Overall Index"),
        ]

        self.category = DatasetCategory
        self.name = "Load Dataset (Iterator)"
        self.icon = "MdSubdirectoryArrowRight"
        self.sub = "Iteration"

        self.type = "iteratorHelper"

        self.side_effects = True

    def run(
        self, path: str, root_dir: str, index: int
    ) -> Tuple[pandas.DataFrame, str, str, str, int]:
        df, df_dir, basename = DatasetReadNode().run(path)

        # Get relative path from root directory passed by Iterator directory input
        rel_path = os.path.relpath(df_dir, root_dir)

        return df, root_dir, rel_path, basename, index


@NodeFactory.register("predikit:dataset:file_iterator")
class DatasetFileIteratorNode(IteratorNodeBase):
    def __init__(self):
        super().__init__()
        self.description = "Iterate over all files in a directory and run the provided nodes on just the dataset files."
        self.inputs = [
            DirectoryInput(),
        ]
        self.outputs = []
        self.category = DatasetCategory
        self.name = "Dataset File Iterator"
        self.default_nodes: List[dict[str, str]] = [
            # TODO: Figure out a better way to do this
            {
                "schemaId": DATASET_ITERATOR_NODE_ID,
            },
        ]

    # pylint: disable=invalid-overridden-method
    async def run(self, directory: str, context: IteratorContext) -> None:
        logger.info(f"Iterating over datasets in directory: {directory}")

        img_path_node_id = context.get_helper(DATASET_ITERATOR_NODE_ID).id

        supported_filetypes = get_available_dataset_formats()

        def walk_error_handler(exception_instance):
            logger.warning(
                f"Exception occurred during walk: {exception_instance} Continuing..."
            )

        just_dataset_files: List[str] = []
        for root, dirs, files in os.walk(
            directory, topdown=True, onerror=walk_error_handler
        ):
            await context.progress.suspend()

            dirs.sort(key=numerical_sort)
            for name in sorted(files, key=numerical_sort):
                filepath = os.path.join(root, name)
                _base, ext = os.path.splitext(filepath)
                if ext.lower() in supported_filetypes:
                    just_dataset_files.append(filepath)

        def before(filepath: str, index: int):
            context.inputs.set_values(
                img_path_node_id, [filepath, directory, index]
            )

        await context.run(just_dataset_files, before)
