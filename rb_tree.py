from typing import Optional
from generic import ABinarySearchTree, BinaryNode


class RBNode(BinaryNode):
    """ Object extends BinaryNode specific for RBTree

    red - if edge to parent is red
    """
    left: 'RBNode'
    right: 'RBNode'

    def __init__(self, key, value=None, prev=None, nxt=None, left=None, right=None, depth: int = 1, external: bool = False, red=True):
        super().__init__(key, value=value, prev=prev, nxt=nxt, left=left, right=right, depth=depth, external=external)
        self.red = red

    @property
    def black(self) -> bool: return not self.red

    def __repr__(self): return f"RBNode( key: {self.key}, red: {self.red} )"


class RBTree(ABinarySearchTree):
    """ Implementation of Red-Black Tree with those invaraints

    1. Every path from root to leaves have same amount of black edges
    2. External nodes - all leaves are black
    3. Two red edges above each other are not allowed
    4. If parent have red edge to child, then this edge is to left

    This variation of RB tree is called left leaning red black tree
    """
    EXTERNAL_NODE = RBNode(0, depth=0, external=True, red=False)
    EXTERNAL_NODE.left = EXTERNAL_NODE
    EXTERNAL_NODE.right = EXTERNAL_NODE

    def __init__(self) -> None:
        self.root = self.EXTERNAL_NODE

    def insert(self, key, value) -> None:
        self.root = self._insert(key, value, self.root)

    def _insert(self, key, value, node: RBNode):
        if node.external:
            new_node = RBNode(key, value, left=self.EXTERNAL_NODE, right=self.EXTERNAL_NODE)
            self._add_node_to_chain(new_node, self._find_lower(self.root, key),
                                    self._find_bigger(self.root, key))

            return new_node

        if node.left.red and node.right.red:
            node.red = True
            node.left.red = node.right.red = False
        if node.key > key:
            node.left = self._insert(key, value, node.left)
        elif node.key == key:
            # key is alread in tree
            pass
        else:
            node.right = self._insert(key, value, node.right)

        return self._fix_llrb_invariants(node)

    def _fix_llrb_invariants(self, node: RBNode) -> RBNode:
        if node.right.red:
            node = self._left_rotation(node)
        if node.left.red and node.left.left.red:
            node = self._right_rotation(node)
        if node.left.red and node.right.red:
            node.red = True
            node.left.red = node.right.red = False
        return node

    def _left_rotation(self, node: RBNode) -> RBNode:
        """ Make left rotation """
        right_node = node.right
        node.right = right_node.left
        right_node.left = node

        node.red, right_node.red = right_node.red, node.red

        return right_node

    def _right_rotation(self, node: RBNode) -> RBNode:
        """  Make right rotation """
        left_node = node.left
        node.left = left_node.right
        left_node.right = node

        node.red, left_node.red = left_node.red, node.red

        return left_node

    def delete(self, key) -> None:
        self.root = self._delete(key, self.root)

    def _delete(self, key, node: RBNode) -> RBNode:
        if node.external:
            return node

        if node.key < key:
            if node.left.red:  # external nodes have only black color
                node = self._right_rotation(node)
            if node.right.black and node.right.left.black and not node.right.external:
                node = self._move_red_right(node)

            node.right = self._delete(key, node.right)
        else:
            if node.key == key and node.right.external:
                # if right node is external, so
                # - if left node is external, so return external node
                # - if left is red node, then this node must be black
                # - if left is black -> cannot occur
                self._remove_node_from_chain(node)
                node.left.red = False
                return node.left
            if node.left.black and node.left.left.black and not node.left.external:
                node = self._move_red_left(node)
            if node.key == key:
                prev_node = node.prev
                self._remove_node_from_chain(node)
                node.left = self._delete(prev_node.key, node.left)
                prev_node.left, prev_node.right = node.left, node.right
                prev_node.red = node.red
                node = prev_node
                self._add_node_to_chain(node, node.prev, node.nxt)
            else:
                node.left = self._delete(key, node.left)

        return self._fix_llrb_invariants(node)

    def _move_red_right(self, node: RBNode) -> RBNode:
        node.red = False
        node.right.red = node.left.red = True

        if node.left.left.red:
            node = self._right_rotation(node)
            node.red = True
            node.left.red = node.right.red = False

        return node

    def _move_red_left(self, node: RBNode) -> RBNode:
        node.red = False
        node.right.red = node.left.red = True

        if node.right.left.red:
            node.right = self._right_rotation(node.right)
            node = self._left_rotation(node)
            node.red = True
            node.right.red = node.left.red = False

        return node

    def __repr__(self):
        return self.makerepr(self.root)

    def makerepr(self, node: RBNode):
        if node.external:
            return "-"
        return f"( {node}, {' '.join( [self.makerepr(x) for x in [node.left, node.right] ] ) } )"

    def validate(self):
        def _validate(node: RBNode, root=False):
            if node.external:
                return (1, True)
            lc, lo = _validate(node.left)
            rc, ro = _validate(node.right)
            valid = root or node.black or (node.red and node.left.black and node.right.black)
            if lc == rc:
                return (lc + (0 if node.red else 1), lo and ro and valid)
            return (-1, False)
        _, ret = _validate(self.root, True)
        return ret and self.EXTERNAL_NODE.black
