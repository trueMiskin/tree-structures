#!/usr/bin/env python3

from ab_tree import ABTree
from avl import AvlTree, AvlNode
import unittest


class TreeGeneric(unittest.TestCase):
    def run_test(self, test_num, tree):
        with open(f"dataset/test{test_num}.in", "r") as fin, open(f"dataset/test{test_num}.out", "r") as fout:
            def checkSequence(node, fce):
                arr = []

                while node is not None:
                    arr.append(node)
                    node = fce(node)

                self.assertEqual(' '.join(str(x.key) for x in arr), fout.readline().strip())

            num_operations = int(fin.readline())

            for _ in range(num_operations):
                #print(_, "------")
                #print(tree)
                _input = fin.readline().split()
                if len(_input) == 1:
                    # don't fail on non-existent second variable
                    _input.append(0)
                operatation, key = map(int, _input)
                if operatation == 0:
                    tree.insert(key, key)
                elif operatation == 1:
                    node = tree.find(key)
                    self.assertEqual(node is not None, fout.readline().strip() == "1")
                elif operatation == 2:
                    tree.delete(key)
                elif operatation == 3:
                    checkSequence(tree.findmin(), lambda x: x.nxt)
                else:
                    checkSequence(tree.findmax(), lambda x: x.prev)


class TestAVLTree(TreeGeneric):
    def right_order_nxt(self, root, correct):
        for x in correct:
            self.assertEqual(root.key, x)
            root = root.nxt
        self.assertEqual(root, None)

    def right_order_prev(self, root, correct):
        for x in correct:
            self.assertEqual(root.key, x)
            root = root.prev
        self.assertEqual(root, None)

    def test_left_rotation(self):
        tree = AvlTree()
        tree.insert(1, 1)
        tree.insert(2, 2)
        tree.insert(3, 3)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    def test_right_rotation(self):
        tree = AvlTree()
        tree.insert(3, 3)
        tree.insert(2, 2)
        tree.insert(1, 1)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    def test_leftside_doublerotation(self):
        tree = AvlTree()
        tree.insert(3, 3)
        tree.insert(1, 1)
        tree.insert(2, 2)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    def test_rightside_doublerotation(self):
        tree = AvlTree()
        tree.insert(1, 1)
        tree.insert(3, 3)
        tree.insert(2, 2)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    def test_nxt_prev(self):
        tree = AvlTree()
        tree.insert(2, 2)
        self.right_order_nxt(tree.root, [2])
        self.right_order_prev(tree.root, [2])

        tree.insert(1, 1)
        self.right_order_nxt(tree.root.left, [1, 2])
        self.right_order_prev(tree.root, [2, 1])

        tree.insert(3, 3)
        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    #     4               2
    #    / \             / \
    #   2   5    ===>   1   4
    #  / \                 /
    # 1   3               3
    def test_right_rotation_after_delete_balance_zero(self):
        tree = AvlTree()
        tree.insert(4, 4)
        tree.insert(2, 2)
        tree.insert(5, 5)
        tree.insert(1, 1)
        tree.insert(3, 3)

        tree.delete(5)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 4)
        self.assertEqual(tree.root.right.left.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3, 4])
        self.right_order_prev(tree.root.right, [4, 3, 2, 1])

    #     3               2
    #    / \             / \
    #   2   4    ===>   1   3
    #  /
    # 1
    def test_right_rotation_after_delete_balance_plus_one(self):
        tree = AvlTree()
        tree.insert(3, 3)
        tree.insert(4, 4)
        tree.insert(2, 2)
        tree.insert(1, 1)

        tree.delete(4)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    #      3                2
    #    /   \             / \
    #   1     4    ===>   1   3
    #    \
    #     2
    def test_leftside_double_rotation_after_delete(self):
        tree = AvlTree()
        tree.insert(3, 3)
        tree.insert(1, 1)
        tree.insert(4, 4)
        tree.insert(2, 2)

        tree.delete(4)

        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

        self.right_order_nxt(tree.root.left, [1, 2, 3])
        self.right_order_prev(tree.root.right, [3, 2, 1])

    #      2              4
    #     / \            / \
    #    1   4   ===>   2   5
    #       / \          \
    #      3   5          3
    def test_left_rotation_after_delete_balance_zero(self):
        tree = AvlTree()
        tree.insert(2, 2)
        tree.insert(4, 4)
        tree.insert(1, 1)
        tree.insert(5, 5)
        tree.insert(3, 3)

        tree.delete(1)

        self.assertEqual(tree.root.key, 4)
        self.assertEqual(tree.root.left.key, 2)
        self.assertEqual(tree.root.left.right.key, 3)
        self.assertEqual(tree.root.right.key, 5)

        self.right_order_nxt(tree.root.left, [2, 3, 4, 5])
        self.right_order_prev(tree.root.right, [5, 4, 3, 2])

    #     2               3
    #    / \             / \
    #   1   3    ===>   2   4
    #        \
    #         4
    def test_left_rotation_after_delete_balance_plus_one(self):
        tree = AvlTree()
        tree.insert(2, 2)
        tree.insert(1, 1)
        tree.insert(3, 3)
        tree.insert(4, 4)

        tree.delete(1)

        self.assertEqual(tree.root.key, 3)
        self.assertEqual(tree.root.left.key, 2)
        self.assertEqual(tree.root.right.key, 4)

    #      2                3
    #    /   \             / \
    #   1     4    ===>   2   4
    #        /
    #       3
    def test_rightside_double_rotation_after_delete(self):
        tree = AvlTree()
        tree.insert(2, 2)
        tree.insert(1, 1)
        tree.insert(4, 4)
        tree.insert(3, 3)

        tree.delete(1)

        self.assertEqual(tree.root.key, 3)
        self.assertEqual(tree.root.left.key, 2)
        self.assertEqual(tree.root.right.key, 4)

        self.right_order_nxt(tree.root.left, [2, 3, 4])
        self.right_order_prev(tree.root.right, [4, 3, 2])

    def test_findmin_findmax(self):
        tree = AvlTree()
        for x in range(10, 20):
            tree.insert(x, x)
        for x in range(9, 0, -1):
            tree.insert(x, x)

        self.assertEqual(tree.findmin().key, 1)
        self.assertEqual(tree.findmax().key, 19)

    def test_fulltest1(self): self.run_test(1, AvlTree())
    def test_fulltest2(self): self.run_test(2, AvlTree())
    def test_fulltest3(self): self.run_test(3, AvlTree())
    def test_fulltest4(self): self.run_test(4, AvlTree())
    def test_fulltest5(self): self.run_test(5, AvlTree())


class TestABTree(TreeGeneric):
    def test_fulltest1(self): self.run_test(1, ABTree(2, 4))
    def test_fulltest2(self): self.run_test(2, ABTree(2, 4))
    def test_fulltest3(self): self.run_test(3, ABTree(2, 4))
    def test_fulltest4(self): self.run_test(4, ABTree(2, 4))
    def test_fulltest5(self): self.run_test(5, ABTree(2, 4))


if __name__ == "__main__":
    unittest.main()
