import asyncio
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

from base_types import (
    InputId,
    NodeId,
    OutputId,
)


class FinishData(TypedDict):
    """
    Represents the data structure for finishing an event.

    Attributes:
        message (str): The message associated with the event.
    """

    message: str


class ImageInputInfo(TypedDict):
    """Represents information about an image input."""

    width: int
    height: int
    channels: int


class DatasetInputInfo(TypedDict):
    """
    Represents the input information for a dataset.

    Attributes:
        columns (List[Any]): The list of column names.
        data (Dict[Any, Any]): The dictionary containing the data.
        index (List[Any]): The list of index values.
        dtype (List[Any]): The list of data types for each column.
        shape (List[int]): The shape of the dataset.
    """

    columns: List[Any]
    data: Dict[Any, Any]
    index: List[Any]
    dtype: List[Any]
    shape: List[int]


InputsDict = Dict[
    InputId, Union[str, int, float, DatasetInputInfo, ImageInputInfo, None]
]


class ExecutionErrorSource(TypedDict):
    """
    Represents the source of an execution error.

    Attributes:
        nodeId (NodeId): The ID of the node where the error occurred.
        schemaId (str): The ID of the schema associated with the node.
        inputs (InputsDict): A dictionary containing the inputs to the node.
    """

    nodeId: NodeId
    schemaId: str
    inputs: InputsDict


class ExecutionErrorData(TypedDict):
    """
    Represents the data associated with an execution error.

    Attributes:
        message (str): The error message.
        exception (str): The exception that caused the error.
        source (Optional[ExecutionErrorSource]): The source of the execution error.
    """

    message: str
    exception: str
    source: Optional[ExecutionErrorSource]


class NodeFinishData(TypedDict):
    finished: List[NodeId]
    nodeId: NodeId
    executionTime: Optional[float]
    data: Optional[Dict[OutputId, Any]]


class IteratorProgressUpdateData(TypedDict):
    percent: float
    iteratorId: NodeId
    running: Optional[List[NodeId]]


class FinishEvent(TypedDict):
    event: Literal["finish"]
    data: FinishData


class ExecutionErrorEvent(TypedDict):
    event: Literal["execution-error"]
    data: ExecutionErrorData


class NodeFinishEvent(TypedDict):
    event: Literal["node-finish"]
    data: NodeFinishData


class IteratorProgressUpdateEvent(TypedDict):
    event: Literal["iterator-progress-update"]
    data: IteratorProgressUpdateData


Event = Union[
    FinishEvent,
    ExecutionErrorEvent,
    NodeFinishEvent,
    IteratorProgressUpdateEvent,
]


class EventQueue:
    """A class representing an event queue."""

    def __init__(self):
        self.queue = asyncio.Queue()

    async def get(self) -> Event:
        """Get the next event from the queue.

        Returns:
            The next event in the queue.
        """
        return await self.queue.get()

    async def put(self, event: Event) -> None:
        """Put an event into the queue.

        Args:
            event: The event to be put into the queue.
        """
        await self.queue.put(event)
