import asyncio


class ConcurrencySafeDict:
    def __init__(self):
        self._data = {}
        self._lock = asyncio.Lock()

    async def __getitem__(self, key):
        async with self._lock:
            return self._data[key]

    async def __setitem__(self, key, value):
        async with self._lock:
            self._data[key] = value

    async def __delitem__(self, key):
        async with self._lock:
            del self._data[key]

    async def keys(self):
        async with self._lock:
            return list(self._data.keys())

    async def items(self):
        async with self._lock:
            return list(self._data.items())

    async def values(self):
        async with self._lock:
            return list(self._data.values())

    async def __len__(self):
        async with self._lock:
            return len(self._data)

    async def __contains__(self, key):
        async with self._lock:
            return key in self._data

    async def __iter__(self):
        async with self._lock:
            return iter(self._data)

    async def clear(self):
        async with self._lock:
            self._data.clear()

    async def get(self, key, default=None):
        async with self._lock:
            return self._data.get(key, default)

    async def pop(self, key, default=None):
        async with self._lock:
            return self._data.pop(key, default)

    async def popitem(self):
        async with self._lock:
            return self._data.popitem()

    async def setdefault(self, key, default=None):
        async with self._lock:
            return self._data.setdefault(key, default)

    async def update(self, *args, **kwargs):
        async with self._lock:
            return self._data.update(*args, **kwargs)

    async def copy(self):
        async with self._lock:
            return self._data.copy()

    async def fromkeys(self, seq, value=None):
        async with self._lock:
            return self._data.fromkeys(seq, value)

    async def __eq__(self, other):
        async with self._lock:
            return self._data == other

    async def __ne__(self, other):
        async with self._lock:
            return self._data != other

    async def __repr__(self):
        async with self._lock:
            return repr(self._data)

    async def __str__(self):
        async with self._lock:
            return str(self._data)
