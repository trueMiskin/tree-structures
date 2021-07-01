from typing import Optional, List, Tuple
from generic import ATree, Node


class ABVertex:
    """ ABVertex is one node in ABTree """
    def __init__(self, keys, children, leaf):
        self.keys: 'List[Node]' = keys
        self.children: 'List[ABVertex]' = children
        self.leaf: bool = leaf

    def __repr__(self):
        return f"ABVertex({', '.join(str(n.key) for n in self.keys)})"


class ABTree(ATree[Node]):
    def __init__(self, a: int, b: int):
        self.root = ABVertex(list(), list(), True)
        self.a = a
        self.b = b

    def insert(self, key, value) -> None:
        new_root, left_vertex, right_vertex = self._insert(key, value, self.root)
        if new_root is not None:
            self.root = ABVertex([new_root], [left_vertex, right_vertex], False)

    def _insert(self, key, value, node: ABVertex) -> Tuple[Optional[Node], Optional[ABVertex], Optional[ABVertex]]:
        """ Insert node to Vertex with given key
            Return key that should be added to parent vertex and left, right vertices to this key
            if vertex is overfull
            Else return None, None, None
        """
        if node.leaf:
            idx = 0
            for idx, n in enumerate(node.keys):
                if key == n.key:
                    # key is alread in tree
                    return (None, None, None)
                if key > n.key:
                    # if loop ends, then i will insert on last position
                    idx += 1
                    continue
                break
            new_node = Node(key, value)
            self._add_node_to_chain(new_node, self._find_lower(self.root, key),
                                    self._find_bigger(self.root, key))

            node.keys.insert(idx, new_node)
        else:
            idx = 0
            for n in node.keys:
                if key > n.key:
                    idx += 1
            mid_node, left_vertex, right_vertex = self._insert(key, value, node.children[idx])
            # mid_node != None then child vertex has got splitted
            if mid_node is not None:
                node.children[idx] = left_vertex             # type: ignore
                node.children.insert(idx + 1, right_vertex)  # type: ignore
                node.keys.insert(idx, mid_node)

        if len(node.keys) == self.b:
            mid = len(node.keys) // 2
            mid_node = node.keys[mid]
            left_vertex = ABVertex(node.keys[:mid], node.children[:mid+1], node.leaf)
            right_vertex = ABVertex(node.keys[mid+1:], node.children[mid+1:], node.leaf)

            return (mid_node, left_vertex, right_vertex)
        return (None, None, None)

    def _find_bigger(self, node: ABVertex, key) -> Optional[Node]:
        """ Find the node with lowest bigger key """
        if node.leaf:
            for n in node.keys:
                if key < n.key:
                    return n
            return None
        else:
            ret = None
            for idx, n in enumerate(node.keys):
                if key < n.key:
                    ret = self._find_bigger(node.children[idx], key)
                    return ret if ret is not None else node.keys[idx]

            return self._find_bigger(node.children[len(node.children) - 1], key)

    def _find_lower(self, node: ABVertex, key) -> Optional[Node]:
        """ Find the node with the largest smaller key """
        if node.leaf:
            ret = None
            for n in node.keys:
                if key > n.key:
                    ret = n
            return ret
        else:
            ret = None
            for idx, n in enumerate(node.keys):
                if key < n.key:
                    ret = self._find_lower(node.children[idx], key)
                    break
            if key > node.keys[len(node.keys) - 1].key:
                idx = len(node.children) - 1
                ret = self._find_lower(node.children[idx], key)
            if idx != 0:
                return ret if ret is not None else node.keys[idx - 1]
            else:
                return ret

    def find(self, key):
        def _find(key, node: ABVertex) -> Optional[Node]:
            for idx, n in enumerate(node.keys):
                if n.key == key:
                    return n
                else:
                    if n.key > key and not node.leaf:
                        return _find(key, node.children[idx])

            if node.leaf:
                return None
            return _find(key, node.children[len(node.children) - 1])

        return _find(key, self.root)

    def delete(self, key) -> None:
        if self._delete(key, self.root) and len(self.root.children) > 0:
            self.root = self.root.children[0]

    def _delete(self, key, vertex: ABVertex) -> bool:
        """ Delete vertex with given key, return True if vertex is underfull"""
        underfull_vertex = False
        key_deleted = False
        for idx, node in enumerate(vertex.keys):
            if node.key == key:
                self._remove_node_from_chain(node)

                if vertex.leaf:
                    vertex.keys.remove(node)
                    return len(vertex.keys) == self.a - 2
                else:
                    # if node is not leaf, then there must prev node
                    replace_node = node.prev
                    underfull_vertex = self._delete(replace_node.key, vertex.children[idx])
                    self._add_node_to_chain(replace_node, replace_node.prev, replace_node.nxt)

                    vertex.keys[idx] = replace_node
                    key_deleted = True
                break
            if node.key > key:
                underfull_vertex = self._delete(key, vertex.children[idx])
                key_deleted = True
                break

        # muzu se zde zavolat po druhe do stromu -> pokud posledni klíč se mi změnil v průběhu mazání
        if vertex.keys[-1].key < key and not key_deleted:
            idx = len(vertex.children) - 1
            underfull_vertex = self._delete(key, vertex.children[idx])

        if underfull_vertex:
            if idx != 0:
                self._solve_underfull(vertex.children[idx], vertex.children[idx - 1], False, vertex, idx - 1)
            else:
                self._solve_underfull(vertex.children[idx], vertex.children[idx + 1], True, vertex, idx)

        return len(vertex.keys) == self.a - 2

    def _solve_underfull(self, underfull_vertex: ABVertex, neighbour_vertex: ABVertex,
                         underfull_vertex_is_left: bool, parent_vertex: ABVertex,
                         parent_idx: int) -> None:
        if len(neighbour_vertex.keys) == self.a - 1:
            # nearly underfull - merge vertexes
            if not underfull_vertex_is_left:
                underfull_vertex, neighbour_vertex = neighbour_vertex, underfull_vertex
            underfull_vertex.keys.extend([parent_vertex.keys.pop(parent_idx), *neighbour_vertex.keys])
            underfull_vertex.children.extend(neighbour_vertex.children)
            parent_vertex.children.pop(parent_idx + 1)
        else:
            if underfull_vertex_is_left:
                underfull_vertex.keys.append(parent_vertex.keys[parent_idx])
                if not underfull_vertex.leaf:
                    underfull_vertex.children.append(neighbour_vertex.children.pop(0))
                parent_vertex.keys[parent_idx] = neighbour_vertex.keys.pop(0)
            else:
                underfull_vertex.keys.insert(0, parent_vertex.keys[parent_idx])
                if not underfull_vertex.leaf:
                    underfull_vertex.children.insert(0, neighbour_vertex.children.pop(-1))
                parent_vertex.keys[parent_idx] = neighbour_vertex.keys.pop(-1)

    def findmin(self):
        def _findmin(vertex: ABVertex) -> Optional[Node]:
            if vertex.leaf:
                return vertex.keys[0] if len(vertex.keys) != 0 else None
            else:
                return _findmin(vertex.children[0])

        return _findmin(self.root)

    def findmax(self):
        def _findmax(vertex: ABVertex) -> Optional[Node]:
            mx_idx = len(vertex.children) - 1
            if vertex.leaf:
                return vertex.keys[mx_idx] if len(vertex.keys) != 0 else None
            else:
                return _findmax(vertex.children[mx_idx])

        return _findmax(self.root)

    def __repr__(self):
        return self.makerepr(self.root)

    def makerepr(self, node: ABVertex):
        return f"( {node}, {' '.join( [self.makerepr(x) for x in node.children] ) } )"
