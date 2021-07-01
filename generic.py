from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic


class Node:
    """ Node structure for holding data

    key - key of node, **must** be compareable
    value - value of node
    prev - closest smaller node
    nxt - closest bigger node
    """
    def __init__(self, key, value=None, prev=None, nxt=None):
        if value is None:
            value = key

        self.key = key
        self.value = value
        self.prev = prev
        self.nxt = nxt

    def __repr__(self):
        return f"Node( key: {self.key}, value: {self.value} )"


class BinaryNode(Node):
    """ Extended structure of node for binary trees

    left - left child node
    right - right child node
    depth - depth of subtree with this node as root
    external - flag says if is it **real** node or helper node
    """
    def __init__(self, key, value=None, prev=None, nxt=None,
                 left=None, right=None,
                 depth: int = 1, external: bool = False):
        super().__init__(key, value, prev, nxt)
        self.left = left
        self.right = right
        self.depth = depth
        self.external = external


T = TypeVar('T', bound=Node)


class ATree(ABC, Generic[T]):
    @abstractmethod
    def find(self, key) -> Optional[T]:
        """ Find node with given key and return it """
        pass

    @abstractmethod
    def insert(self, key, value) -> None:
        """ Insert node with given key and value """
        pass

    @abstractmethod
    def delete(self, key) -> None:
        """ Delete node with given key """
        pass

    @abstractmethod
    def findmin(self) -> Optional[T]:
        """ Return node with the smallest key or None (tree empty) """
        pass

    @abstractmethod
    def findmax(self) -> Optional[T]:
        """ Return node with the biggest key or None (tree empty) """
        pass

    def _add_node_to_chain(self, node: T,
                           prev_node: Optional[T], nxt_node: Optional[T]):
        node.prev, node.nxt = prev_node, nxt_node
        if prev_node is not None:
            prev_node.nxt = node
        if nxt_node is not None:
            nxt_node.prev = node

    def _remove_node_from_chain(self, node: T):
        prev_node = node.prev
        nxt_node = node.nxt
        if prev_node is not None:
            prev_node.nxt = nxt_node
        if nxt_node is not None:
            nxt_node.prev = prev_node


BN = TypeVar('BN', bound=BinaryNode)


class ABinarySearchTree(ATree[BN]):
    root: BN

    def find(self, key) -> Optional[BN]:
        def _find(key, node: BN) -> Optional[BN]:
            if node.external:
                return None

            if node.key == key:
                return node
            elif node.key < key:
                return _find(key, node.right)
            else:
                return _find(key, node.left)
        return _find(key, self.root)

    def _find_bigger(self, node: BN, key) -> Optional[BN]:
        if node.external:
            return None

        if key < node.key:
            ret = self._find_bigger(node.left, key)
            if ret is None:
                return node
            return ret
        else:
            return self._find_bigger(node.right, key)

    def _find_lower(self, node: BN, key) -> Optional[BN]:
        if node.external:
            return None

        if key > node.key:
            ret = self._find_lower(node.right, key)
            if ret is None:
                return node
            return ret
        else:
            return self._find_lower(node.left, key)

    def findmin(self) -> Optional[BN]:
        def _findmin(node):
            if node == self.EXTERNAL_NODE:
                return None
            if node.left == self.EXTERNAL_NODE:
                return node
            else:
                return _findmin(node.left)

        return _findmin(self.root)

    def findmax(self) -> Optional[BN]:
        def _findmax(node):
            if node == self.EXTERNAL_NODE:
                return None
            if node.right == self.EXTERNAL_NODE:
                return node
            else:
                return _findmax(node.right)
        return _findmax(self.root)
