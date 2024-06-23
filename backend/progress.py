from abc import (
    ABC,
    abstractmethod,
)
import asyncio


class Aborted(Exception):
    """Exception raised when a process is aborted."""

    pass


class ProgressToken(ABC):
    @property
    @abstractmethod
    def paused(self) -> bool:
        pass

    @property
    @abstractmethod
    def aborted(self) -> bool:
        pass

    @abstractmethod
    async def suspend(self) -> None:
        """
        If the operation was aborted, this method will throw an `Aborted` exception.
        If the operation is paused, this method will wait until the operation is resumed or aborted.
        """


class ProgressController(ProgressToken):
    """A class that represents a progress controller.

    This class provides methods to control the progress of a task, such as pausing, resuming, and aborting.

    Attributes:
        __paused (bool): A boolean indicating whether the progress is paused.
        __aborted (bool): A boolean indicating whether the progress is aborted.
    """

    def __init__(self):
        self.__paused: bool = False
        self.__aborted: bool = False

    @property
    def paused(self) -> bool:
        """bool: Indicates whether the progress is paused."""
        return self.__paused

    @property
    def aborted(self) -> bool:
        """bool: Indicates whether the progress is aborted."""
        return self.__aborted

    def pause(self):
        """Pauses the progress."""
        self.__paused = True

    def resume(self):
        """Resumes the progress."""
        self.__paused = False

    def abort(self):
        """Aborts the progress."""
        self.__aborted = True

    async def suspend(self) -> None:
        """Suspends the progress.

        Raises:
            Aborted: If the progress is aborted while suspended.
        """
        if self.aborted:
            raise Aborted()

        while self.paused:
            await asyncio.sleep(0.1)
            if self.aborted:
                raise Aborted()
