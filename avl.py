from typing import Optional, Type
from generic import ABinarySearchTree, BinaryNode


class AvlNode(BinaryNode):
    """ Object extends BinaryNode specific for AvlTree """
    nxt: 'AvlNode'
    prev: 'AvlNode'

    def update(self):
        self.depth = max(self.left.depth, self.right.depth) + 1

    @property
    def balance(self):
        """ Return balance of tree
        -1 -- right subtree has bigger depth
        0  -- left and right subtree has same depth
        1  -- left subtree has bigger depth
        """
        return self.left.depth - self.right.depth


class AvlTree(ABinarySearchTree):
    EXTERNAL_NODE = AvlNode(0, depth=0, external=True)
    EXTERNAL_NODE.left = EXTERNAL_NODE
    EXTERNAL_NODE.right = EXTERNAL_NODE

    def __init__(self):
        self.root = self.EXTERNAL_NODE

    def insert(self, key, value) -> None:
        self.root = self._insert(key, value, self.root)

    def _insert(self, key, value, node: AvlNode) -> AvlNode:
        if node.external:
            new_node = AvlNode(key, value, left=self.EXTERNAL_NODE, right=self.EXTERNAL_NODE)
            nxt_node = self._find_bigger(self.root, key)
            if nxt_node is not None:
                new_node.nxt = nxt_node
                nxt_node.prev = new_node

            prev_node = self._find_lower(self.root, key)
            if prev_node is not None:
                new_node.prev = prev_node
                prev_node.nxt = new_node
            return new_node

        if key == node.key:
            # key found - nothing to do
            return node
        elif key < node.key:
            node.left = self._insert(key, value, node.left)
        else:
            node.right = self._insert(key, value, node.right)

        left_depth = node.left.depth
        right_depth = node.right.depth

        if abs(left_depth - right_depth) <= 1:
            # everything is OK
            pass
        else:
            if left_depth > right_depth:
                if node.left.balance == 1:
                    node = self._rotation(node, left_rotation=False)
                elif node.left.balance == -1:
                    node = self._double_rotation(node, left_side=True)
                else:
                    # this state cannot accur
                    pass
            else:
                if node.right.balance == -1:
                    node = self._rotation(node, left_rotation=True)
                elif node.right.balance == 1:
                    node = self._double_rotation(node, left_side=False)
                else:
                    # this state cannot accur
                    pass

        node.update()
        return node

    def delete(self, key) -> None:
        self.root = self._delete(key, self.root)

    def _delete(self, key, node: AvlNode) -> AvlNode:
        if node.external:
            return node
        if node.key == key:
            prev_node = node.prev
            nxt_node = node.nxt
            if prev_node is not None:
                prev_node.nxt = nxt_node
            if nxt_node is not None:
                nxt_node.prev = prev_node

            if node.left == self.EXTERNAL_NODE:
                return node.right
            elif node.right == self.EXTERNAL_NODE:
                return node.left
            else:
                replace_node: AvlNode = self._find_lower(node, key)  # type: ignore
                node.left = self._delete(replace_node.key, node.left)
                if replace_node.prev is not None:
                    replace_node.prev.nxt = replace_node
                if replace_node.nxt is not None:
                    replace_node.nxt.prev = replace_node
                replace_node.left = node.left
                replace_node.right = node.right
                node = replace_node

        elif node.key > key:
            node.left = self._delete(key, node.left)
        else:
            node.right = self._delete(key, node.right)

        left_depth = node.left.depth
        right_depth = node.right.depth
        if abs(left_depth - right_depth) <= 1:
            # everything is OK
            pass
        else:
            if left_depth > right_depth:
                if node.left.balance == 1 or node.left.balance == 0:
                    node = self._rotation(node, left_rotation=False)
                else:
                    node = self._double_rotation(node, left_side=True)
            else:
                if node.right.balance == -1 or node.right.balance == 0:
                    node = self._rotation(node, left_rotation=True)
                else:
                    node = self._double_rotation(node, left_side=False)

        node.update()
        return node

    def _rotation(self, subtree_root: AvlNode, left_rotation=True) -> AvlNode:
        """Makes single rotation, update node depth, return new root of subtree"""
        if left_rotation:
            right_node = subtree_root.right
            subtree_root.right = right_node.left
            right_node.left = subtree_root

            subtree_root.update()
            right_node.update()

            return right_node
        else:
            left_node = subtree_root.left
            subtree_root.left = left_node.right
            left_node.right = subtree_root

            subtree_root.update()
            left_node.update()

            return left_node

    def _double_rotation(self, subtree_root: AvlNode, left_side=True) -> AvlNode:
        """Makes double rotation from single rotations, return new root of subtree"""
        if left_side:
            subtree_root.left = self._rotation(subtree_root.left)
            return self._rotation(subtree_root, left_rotation=False)
        else:
            subtree_root.right = self._rotation(subtree_root.right, left_rotation=False)
            return self._rotation(subtree_root)
