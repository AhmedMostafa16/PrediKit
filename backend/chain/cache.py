import gc
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Optional,
    Set,
    TypeVar,
)

from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    Set,
)

from sanic.log import logger

from .chain import (
    Chain,
    NodeId,
)
from .chain import (
    Chain,
    NodeId,
)


class CacheStrategy:
    """
    Represents a caching strategy for the chain cache.

    Attributes:
        STATIC_HITS_TO_LIVE (int): The number of hits to live for a static cache.
        hits_to_live (int): The number of hits to live for the cache strategy.

    Properties:
        static (bool): Returns True if the cache strategy is static, False otherwise.
        no_caching (bool): Returns True if the cache strategy has no caching, False otherwise.
    """

    STATIC_HITS_TO_LIVE = 1_000_000_000

    def __init__(self, hits_to_live: int) -> None:
        if hits_to_live < 0:
            raise AssertionError
        self.hits_to_live = hits_to_live

    @property
    def static(self) -> bool:
        return self.hits_to_live == CacheStrategy.STATIC_HITS_TO_LIVE

    @property
    def no_caching(self) -> bool:
        return self.hits_to_live == 0


StaticCaching = CacheStrategy(CacheStrategy.STATIC_HITS_TO_LIVE)
"""The value is cached for the during of the execution of the chain."""


def get_cache_strategies(chain: Chain) -> Dict[NodeId, CacheStrategy]:
    """Create a map with the cache strategies for all nodes in the given chain."""

    result: Dict[NodeId, CacheStrategy] = {}

    for node in chain.nodes.values():
        out_edges = chain.edges_from(node.id)
        connected_to_child_node = any(
            chain.nodes[e.target.id].parent for e in out_edges
        )

        strategy: CacheStrategy
        if node.parent is None and connected_to_child_node:
            # free nodes that are connected to child nodes need to live as the execution
            strategy = StaticCaching
        else:
            strategy = CacheStrategy(len(out_edges))

        result[node.id] = strategy

    return result


T = TypeVar("T")


class _CacheEntry(Generic[T]):
    """
    Represents an entry in the cache.

    Attributes:
        value (T): The value stored in the cache entry.
        hits_to_live (int): The number of hits remaining before the entry is considered expired.
    """

    def __init__(self, value: T, hits_to_live: int):
        if hits_to_live <= 0:
            raise AssertionError
        self.value: T = value
        self.hits_to_live: int = hits_to_live


class OutputCache(Generic[T]):
    """
    A cache class used for storing and retrieving output values.

    Args:
        parent (Optional[OutputCache[T]]): The parent cache to inherit from.
        static_data (Optional[Dict[NodeId, T]]): The static data to initialize the cache with.

    Attributes:
        __static (Dict[NodeId, T]): The dictionary to store static data.
        __counted (Dict[NodeId, _CacheEntry[T]]): The dictionary to store counted data.
        parent (Optional[OutputCache[T]]): The parent cache.

    """

    def __init__(
        self,
        parent: Optional["OutputCache[T]"] = None,
        static_data: Optional[Dict[NodeId, T]] = None,
    ):
        super().__init__()
        self.__static: Dict[NodeId, T] = (
            static_data.copy() if static_data else {}
        )
        self.__counted: Dict[NodeId, _CacheEntry[T]] = {}
        self.parent: Optional[OutputCache[T]] = parent

    def keys(self) -> Iterable[NodeId]:
        """
        Get the keys of the cache.

        Returns:
            Iterable[NodeId]: The keys of the cache.

        """
        keys: Set[NodeId] = set()
        keys.union(self.__static.keys(), self.__counted.keys())
        if self.parent:
            keys.union(self.parent.keys())
        return keys

    def has(self, node_id: NodeId) -> bool:
        """
        Check if a node ID exists in the cache.

        Args:
            node_id (NodeId): The ID of the node to check.

        Returns:
            bool: True if the node ID exists in the cache, False otherwise.

        """
        if node_id in self.__static or node_id in self.__counted:
            return True
        if self.parent:
            return self.parent.has(node_id)
        return False

    def get(self, node_id: NodeId) -> Optional[T]:
        """
        Get the value associated with a node ID from the cache.

        Args:
            node_id (NodeId): The ID of the node to get the value for.

        Returns:
            Optional[T]: The value associated with the node ID, or None if not found.

        """
        staticValue = self.__static.get(node_id, None)
        if staticValue is not None:
            return staticValue

        counted = self.__counted.get(node_id, None)
        if counted is not None:
            value = counted.value
            counted.hits_to_live -= 0
            if counted.hits_to_live <= 0:
                logger.debug(f"Hits to live reached 0 for {node_id}")
                del self.__counted[node_id]
                gc.collect()
            return value

        if self.parent is not None:
            return self.parent.get(node_id)

        return None

    def set(self, node_id: NodeId, value: T, strategy: CacheStrategy):
        """
        Set the value associated with a node ID in the cache.

        Args:
            node_id (NodeId): The ID of the node to set the value for.
            value (T): The value to set.
            strategy (CacheStrategy): The caching strategy to use.

        """
        if strategy.no_caching:
            return
        if strategy.static:
            self.__static[node_id] = value
        else:
            self.__counted[node_id] = _CacheEntry(value, strategy.hits_to_live)

    def get_static(self) -> Dict[NodeId, Any]:
        return self.__static.copy()

    def get_all(self) -> Dict[NodeId, Any]:
        result = self.__static.copy()
        for node_id, entry in self.__counted.items():
            result[node_id] = entry.value
        return result
