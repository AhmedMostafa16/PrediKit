from typing import Any, Optional


class Result[T]:
    """
    A generic class representing the result of an operation that can either succeed with a value or fail with an error.
    """

    def __init__(self, value: Optional[T] = None, error: Optional[Any] = None) -> None:
        self.value: Optional[T] = value
        self.error: Optional[Any] = error

    @property
    def success(self) -> bool:
        return self.error is None
