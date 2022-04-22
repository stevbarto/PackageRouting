class Node:
    """
    Node class for the linked list and graph data structures.
    """
    next_node = None

    def __init__(self, last_node, item, value):
        self.last_node = last_node
        self.item = item
        self.value = value

    def get_value(self):
        return self.value