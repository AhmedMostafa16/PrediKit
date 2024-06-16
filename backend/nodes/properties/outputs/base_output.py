from typing import (
    Literal,
    Union,
)

from base_types import OutputId

from .. import expression

OutputKind = Literal[
    "dataset",
    "image",
    "large-image",
    "text",
    "directory",
    "generic",
    "plot",
    "list",
]


class BaseOutput:
    def __init__(
        self,
        output_type: expression.ExpressionJson,
        label: str,
        kind: OutputKind = "generic",
        has_handle: bool = True,
    ):
        """
        Initializes a BaseOutput object.

        Args:
            output_type (expression.ExpressionJson): The output type.
            label (str): The label of the output.
            kind (OutputKind, optional): The kind of the output. Defaults to "generic".
            has_handle (bool, optional): Whether the output has a handle. Defaults to True.
        """
        self.output_type: expression.ExpressionJson = output_type
        self.label: str = label
        self.id: OutputId = OutputId(-1)
        self.never_reason: Union[str, None] = None
        self.kind: OutputKind = kind
        self.has_handle: bool = has_handle

    def toDict(self):
        """
        Converts the BaseOutput object to a dictionary.

        Returns:
            dict: The BaseOutput object as a dictionary.
        """
        return {
            "id": self.id,
            "type": self.output_type,
            "label": self.label,
            "neverReason": self.never_reason,
            "kind": self.kind,
            "hasHandle": self.has_handle,
        }

    def with_id(self, output_id: Union[OutputId, int]):
        """
        Sets the ID of the BaseOutput object.

        Args:
            output_id (Union[OutputId, int]): The ID of the output.

        Returns:
            BaseOutput: The BaseOutput object with the updated ID.
        """
        self.id = OutputId(output_id)
        return self

    def with_never_reason(self, reason: str):
        """
        Sets the never reason of the BaseOutput object.

        Args:
            reason (str): The never reason.

        Returns:
            BaseOutput: The BaseOutput object with the updated never reason.
        """
        self.never_reason = reason
        return self

    def __repr__(self):
        """
        Returns a string representation of the BaseOutput object.

        Returns:
            str: The string representation of the BaseOutput object.
        """
        return str(self.toDict())

    def __iter__(self):
        """
        Iterates over the items of the BaseOutput object.

        Yields:
            tuple: The key-value pairs of the BaseOutput object.
        """
        yield from self.toDict().items()

    @staticmethod
    def get_broadcast_data(_value):
        """
        Returns the broadcast data of the BaseOutput object.

        Args:
            _value: The value.

        Returns:
            None: The broadcast data.
        """
        return None
