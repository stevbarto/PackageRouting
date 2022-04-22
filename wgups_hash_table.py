import wgups_package

# hashTable using chaining for collision handling
# @author Steven Barton
from linked_list import LinkedList


class hashTable:
    def __init__(self, start_size, threshold):
        self.size = 0
        self.listSize = start_size
        self.table = []
        self.threshold = threshold
        for i in range(start_size):
            self.table.append(LinkedList())

    def insert(self, id, address, deadline, city, state, zip_code, weight, status):

        # Create a new package to insert based on the provided parameters
        new_package = wgups_package.package(id, address, deadline, city, state, zip_code, weight, status)

        # Identify a bucket index by hashing the key
        index = self.hash(new_package, self.listSize)

        # Insert the item in the bucket and increment size

        self.table[index].insert(new_package, 0)
        self.size = self.size + 1

        # If the bucket size is over the threshold after insertion, grow and rehash the table.
        if len(self.table[index]) > self.threshold:
            self.reHash()

    def search(self, id, address, deadline, city, state, zip_code, weight, status):
        # Create a working package using the parameters
        item = wgups_package.package(id, address, deadline, city, state, zip_code, weight, status)

        # Hash the key to get the index
        index = self.hash(item, self.listSize)

        # Compare each item in the bucket and return the one with the matching key
        #  If the bucket does not contain the matching key, return nothing, throw exception
        reference_list = self.table[index]
        reference_node = reference_list.base_node.next_node

        for i in range(reference_list.size):
            if reference_node.item.get_id() == item.get_id():
                return reference_node.item
            elif reference_node.item is None:
                raise LookupError("Item not found")

            reference_node = reference_node.next_node

    def remove(self, id, address, deadline, city, state, zip_code, weight, status):
        item = wgups_package.package(id, address, deadline, city, state, zip_code, weight, status)

        # definition of remove
        index = self.hash(item, self.listSize)

        # If the index contains the matching key, remove that item and decrease size
        #  If the bucket does not contain the key, throw exception
        reference_list = self.table[index]
        reference_node = reference_list.base_node.next_node

        for i in range(reference_list.size):
            if reference_node.item.get_id() == item.get_id():
                self.table[index].delete(item)
                self.size = self.size - 1
            else:
                raise LookupError("Item not found")

    def hash(self, package, size):
        # TODO: How to determine a hash function for the insert, search, delete functions
        # Determine a unique key, probably the unique ID and weight combined
        key = package.get_id() + package.get_weight()

        # Use the ID and weight as input to create unique hashes, need a good algorithm here
        hash_code = key % size
        return hash_code

    def reHash(self):
        # Swap out existing table and create a new one
        newTable = []
        oldTable = self.table

        # Increase the list size and populate the new table
        self.listSize = self.listSize * 2
        for i in range(self.listSize):
            newTable.append(LinkedList())

        # Put new table in place
        self.table = newTable
        self.size = 0

        # Iterate over the old table and re-insert the items into the new table.
        for i in range(len(oldTable)):
            if oldTable[i].size > 0:
                for j in range(oldTable[i].size):
                    same_item = oldTable[i][j]
                    self.insert(same_item.get_id(), same_item)
