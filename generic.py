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
        self.prev: 'Node' = prev
        self.nxt: 'Node' = nxt

    def __repr__(self):
        return f"Node( key: {self.key}, value: {self.value} )"
