import asyncio
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

from base_types import (
    InputId,
    NodeId,
    OutputId,
)


class FinishData(TypedDict):
    message: str


class DatasetInputInfo(TypedDict):
    columns: List[Any]
    data: Dict[Any, Any]
    index: List[Any]
    dtype: List[Any]
    shape: List[int]


InputsDict = Dict[InputId, Union[str, int, float, DatasetInputInfo, None]]


class ExecutionErrorSource(TypedDict):
    nodeId: NodeId
    schemaId: str
    inputs: InputsDict


class ExecutionErrorData(TypedDict):
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
