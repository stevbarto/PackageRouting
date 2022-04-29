import wgups_package
import wgups_package


class Node:
    """
    Node class for the linked list and graph data structures.
    """
    next_node = None
    assigned = 0

    def __init__(self, last_node, item, value):
        self.last_node = last_node
        self.item = item
        self.value = value

    def get_value(self):
        return self.value

    def get_item(self):
        return self.item

    def set_assigned(self):
        if self.assigned == 0:
            self.assigned = 1
        else:
            self.assigned = 1