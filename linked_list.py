from node import Node


class LinkedList:
    """
    A class representing a simple doubly linked list object to be used in the WGUPS hash table and graph data
    structures. This list represents a bucket for chaining in the hash table and a node in the graph.

    Attributes
    ----------
    size : int
        An integer value tracking the current number of objects in the list.
    base_node : Node
        A Node object which marks the head end of the linked list.
    tail_node : Node
        A Node object which marks the tail end of the linked list.
    current_node : Node
        A marker which indicates where the current Node is during insertion and deletion.

    Methods
    -------


    """

    def __init__(self):
        self.size = 0
        self.base_node = Node(None, None, -1)
        self.tail_node = Node(None, None, -2)
        self.base_node.next_node = self.tail_node
        self.tail_node.last_node = self.base_node
        self.current_node = self.base_node

    def __getitem__(self, index):
        base_search_node = self.base_node

        for i in range(index):
            base_search_node = base_search_node.next_node

        return base_search_node.item

    def __len__(self):
        return self.size

    def insert(self, item, value):
        """
        Insert method for the linked list structure used for separate chaining in the wgups_hash_table.
        :param item: The wgups_package.Package object to be inserted into the linked list
        :param weight: int weight value user for distances or weights in a graph, for hash table this can be arbitrary
        :return: No return value
        """
        # Create a new node with the parameter package
        new_node = Node(self.current_node, item, value)

        # Update the next and last node values for the new node and its last node
        self.current_node.next_node = new_node
        new_node.last_node = self.current_node

        # Update the current_node to be the new node
        self.current_node = new_node

        # Update the new current node and the tail node to reference each other
        self.current_node.next_node = self.tail_node
        self.tail_node.last_node = self.current_node

        # Increment the size of the linked list
        self.size = self.size + 1

    def delete(self, item):
        """
        Delete method for the linked list used for separate chaining in the wgups_hash_table.
        :param item: Package object which needs to be deleted.
        :return: 0 if nothing is deleted, 1 when a delete is carried out
        """

        # Delete cases:
        # Case 1: Delete from an empty list, return 0
        # Case 2: Delete when both next and last nodes are None type ref nodes (1 item), return 1
        # Case 3: Last node is a None type ref node, next node is valid node, return 1
        # Case 4: Last node is a valid node, next node is a None type ref node, return 1
        # Case 5: Both Last and next are valid nodes, return 1
        # Case 6: Package does not exist, return 0

        # Set the reference nodes for list traversal
        base_ref_node = self.base_node
        top_ref_node = self.current_node

        # Case 1
        if self.size == 0:
            return 0

        # Case 2
        if self.size == 1:
            base_ref_node = base_ref_node.next_node

            if base_ref_node.item.get_id() == item.get_id():
                self.__init__()
                return 1

        # Move the ref nodes off the placeholder nodes for package comparison
        base_ref_node = base_ref_node.next_node

        # Determine the number of iterations based on the length of the list
        if self.size % 2 == 0:
            iterations = int((self.size / 2) + 1)
        else:
            iterations = int((self.size / 2) + 2)

        # Iterate over the list to look for the item in cases 3-5
        for i in range(iterations):
            if base_ref_node.item.get_id() == item.get_id():
                # Case 3
                # Case 4
                # Case 5
                base_ref_node.last_node.next_node = base_ref_node.next_node
                base_ref_node.next_node.last_node = base_ref_node.last_node
                self.size = self.size - 1
                self.current_node = self.tail_node.last_node
                return 1

            if top_ref_node.item.get_id() == item.get_id():
                # Case 3
                # Case 4
                # Case 5
                top_ref_node.last_node.next_node = top_ref_node.next_node
                top_ref_node.next_node.last_node = top_ref_node.last_node
                self.size = self.size - 1
                self.current_node = self.tail_node.last_node
                return 1

            if base_ref_node.next_node.item is not None:
                base_ref_node = base_ref_node.next_node
            if top_ref_node.last_node.item is not None:
                top_ref_node = top_ref_node.last_node

        # Case 6
        return 0

    def contains(self, item):
        base_ref_node = self.base_node.next_node
        top_ref_node = self.current_node

        # TODO: This loop goes clear through from both ends, need a more efficient way...
        while base_ref_node.item is not None and top_ref_node.item is not None:
            if base_ref_node.item.get_id() == item.get_id() or top_ref_node.item.get_id() == item.get_id():
                return 1

            base_ref_node = base_ref_node.next_node
            top_ref_node = top_ref_node.last_node

        return 0

    def get_item(self, id):
        check_node = self.base_node.next_node

        while check_node.item is not None:
            if check_node.item.get_id() == id:
                return check_node

            check_node = check_node.next_node

    def get_first_node(self):
        return self.base_node.next_node
