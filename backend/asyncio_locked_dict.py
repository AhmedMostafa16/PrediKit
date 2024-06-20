"""Provide a single class derived from dict to allow thread safe and mutable iterations through a lock."""

import asyncio
import itertools

__all__ = ["AsyncioLockedDict"]


# Use basestring name lookup test to adapt to python version
try:
    # noinspection PyCompatibility
    base_str = basestring  # type: ignore
    items = "iteritems"  # from here on we are python < v3
except NameError:  # ... below section applies to python v3+
    base_str = str, bytes, bytearray
    items = "items"


class AsyncioLockedDict(dict):
    """
    A dictionary subclass that provides thread-safe access using asyncio Lock.

    This class extends the built-in `dict` class and adds support for asynchronous
    locking using `asyncio.Lock`. It ensures that the dictionary operations are
    thread-safe when used in an asynchronous context.

    Attributes:
        _lock (asyncio.Lock): The lock used to synchronize access to the dictionary.

    Methods:
        __init__: Initializes the AsyncioLockedDict object.
        __enter__: Enters the context block and acquires the lock.
        __exit__: Exits the context block and releases the lock.
        __getstate__: Enables pickling inside context blocks.
        __setstate__: Restores the instance from pickle.
        __getitem__: Retrieves the value associated with the given key.
        __setitem__: Sets the value associated with the given key.
        __delitem__: Deletes the key-value pair with the given key.
        get: Retrieves the value associated with the given key, with a default value.
        setdefault: Retrieves the value associated with the given key, with a default value.
        pop: Removes and returns the value associated with the given key.
        update: Updates the dictionary with the key-value pairs from the given mapping or iterable.
        __contains__: Checks if the dictionary contains the given key.
        fromkeys: Creates a new dictionary with the specified keys and a default value.

    Example:
        >>> async def main():
        ...     async with AsyncioLockedDict(a=1) as d:
        ...         d["b"] = 2
        ...         d["c"] = 3
        ...         print(d)
        ...
        >>> asyncio.run(main())
        {'a': 1, 'b': 2, 'c': 3}

    """

    __slots__ = ("_lock",)  # no __dict__ - that would be redundant

    @staticmethod
    def _process_args(map_or_it=(), **kwargs):
        """Custom made helper for this class."""
        if hasattr(map_or_it, items):
            map_or_it = getattr(map_or_it, items)()
        it_chain = itertools.chain
        return (
            (k, v) for k, v in it_chain(map_or_it, getattr(kwargs, items)())
        )

    def __init__(self, mapping=(), **kwargs):
        """Base (dict) accepts mappings or iterables as first argument."""
        super(AsyncioLockedDict, self).__init__(
            self._process_args(mapping, **kwargs)
        )
        self._lock = asyncio.Lock()

    async def __enter__(self):
        """Context manager enter the block, acquire the lock."""
        await self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit the block, release the lock."""
        self._lock.release()

    def __getstate__(self):
        """Enable Pickling inside context blocks,
        through inclusion of the slot entries without the lock."""
        return {
            slot: getattr(self, slot)
            for slot in self.__slots__
            if hasattr(self, slot) and slot != "_lock"
        }

    def __setstate__(self, state):
        """Restore the instance from pickle including the slot entries,
        without addition of a fresh lock.
        """
        for slot, value in getattr(state, items)():
            setattr(self, slot, value)
        self._lock = asyncio.Lock()

    def __getitem__(self, k):
        """For now plain delegation of getitem method to base class."""
        return super(AsyncioLockedDict, self).__getitem__(k)

    def __setitem__(self, k, v):
        """For now plain delegation of setitem method to base class."""
        return super(AsyncioLockedDict, self).__setitem__(k, v)

    def __delitem__(self, k):
        """For now plain delegation of del method to base class."""
        return super(AsyncioLockedDict, self).__delitem__(k)

    def get(self, k, default=None):
        """For now plain delegation of get method to base class."""
        return super(AsyncioLockedDict, self).get(k, default)

    def setdefault(self, k, default=None):
        """For now plain delegation of setdefault method to base class."""
        return super(AsyncioLockedDict, self).setdefault(k, default)

    def pop(self, k, d=None):
        """For now plain delegation of pop method to base class."""
        return super(AsyncioLockedDict, self).pop(k, d)

    def update(self, map_or_it=(), **kwargs):
        """Ensure processing of mappings or iterables as first argument."""
        super(AsyncioLockedDict, self).update(
            self._process_args(map_or_it, **kwargs)
        )

    def __contains__(self, k):
        """For now plain delegation of contains method to base class."""
        return super(AsyncioLockedDict, self).__contains__(k)

    @classmethod
    def fromkeys(cls, seq, value=None):
        """For now plain delegation of fromkeys class method to base."""
        return super(AsyncioLockedDict, cls).fromkeys(seq, value)
