# tree-structures

This project implements most known balanced search trees: AVL tree,
AB tree and Red-Black tree (specificly left leaning red-black tree).

## Interface

All trees implements this methods:
* find: find key in tree and return node with this key or None
* insert: insert key to tree, if key exists in tree nothing happends
* delete: delete key from tree, if key doesn't exist nothing happends
* findmin: return node with the lowest key or None if tree is empty
* findmax: return node with the biggest key or None if tree is empty

All nodes have `prev` and `nxt` field. The `prev` contains the node
which have the biggest smaller key. The `nxt` otherwise contains the
node which have the smallest bigger key.

## Short information about structures

* AVL tree: Implements classic binary search tree with rotations
to keep tree balanced (balance invariant: | depth of left subtree - depth of right tree | <= 1)
* AB tree: Balance search tree which have more keys in one vertex
(atleast a-1 keys and at most b-1 keys, the root of node must have atleast
one key if not empty).
Invariant for AB trees: All leaf nodes have same depth. New added key is
always inserted to the leaf. If node is overfull, then vertex is splitted
on new two vertices and middle key is inserted to parent vertex.
When we delete the key the vertices can be underfull, then
we borrow key from neighbour vertex or even merge neighnour vertex.
* LLRB tree (left leaning red-black tree): Binary search tree with those
invariants:
    1. Every path from root to leaves have same amount of black edges
    2. External nodes - all leaves are black
    3. Two red edges above each other are not allowed
    4. If parent have red edge to child, then this edge is to left

## Testing

This project have some basic tests but most tests uses pregenerated
tests from `dataset` directory. In this directory is `genTests.py` file
which generate this input and output files for testing.
