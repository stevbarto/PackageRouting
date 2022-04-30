import wgups_package


class hashTable:
    def __init__(self, start_size, threshold):
        self.size = 0
        self.listSize = start_size
        self.table = []
        self.threshold = threshold
        for i in range(start_size):
            self.table.append([])

    def insert(self, id, package):

        if self.size == int(self.listSize * 0.8):
            self.reHash()

        # Identify a bucket index by hashing the key
        index = self.hash(id)

        # Insert the item in the bucket and increment size if the bucket is not full
        # if len(self.table[index]) < self.threshold:
        #    self.table[index].append(package)
        #    self.size = self.size + 1
        # If the bucket size is over the threshold after insertion, grow and rehash the table.
        i = 0
        probe_index = index
        while i < self.listSize:
            # probe_index = probe_index + 1
            probe_index = probe_index + i * i
            while probe_index >= self.listSize:
                probe_index = probe_index - self.listSize

            if len(self.table[probe_index]) < self.threshold:
                self.table[probe_index].append(package)
                self.size = self.size + 1
                return

                # elif probe_index >= self.listSize:
                #    if len(self.table[probe_index]) < self.threshold:
                #        self.table[probe_index].append(package)
                #        self.size = self.size + 1
                #        return
            # TODO: This should track if the value was inserted at the end of looping if not, rehash and do again
            # TODO: Rehash should ensure there is some extra empty indices at all times for probing to be fast
            i = i + 1

        self.reHash()
        self.insert(id, package)

    def search(self, package_id):
        # Create a working package using the parameters
        item = package_id

        # Hash the key to get the index
        index = self.hash(item)

        # Compare each item in the bucket and return the one with the matching key
        #  If the bucket does not contain the matching key, return nothing, throw exception
        reference_list = self.table[index]

        # for i in range(len(reference_list)):
        #    package = reference_list[i]
        #    if package.get_id() == item:
        #        return package

        j = 0
        probe_index = index
        while j < self.listSize:
            # probe_index = probe_index + 1
            probe_index = probe_index + j * j
            while probe_index >= self.listSize:
                probe_index = probe_index - self.listSize

            reference_list = self.table[probe_index]

            for i in range(len(reference_list)):
                package = reference_list[i]

                if package.get_id() == item:
                    return package

            # if probe_index >= self.listSize:
            #    probe_index = probe_index - self.listSize
            #    reference_list = self.table[probe_index]
            #    for i in range(len(reference_list)):
            #        package = reference_list[i]
            #        if package.get_id() == item:
            #            return package
            j = j + 1

    def remove(self, package_id):
        item = package_id

        # definition of remove
        index = self.hash(item)

        # If the index contains the matching key, remove that item and decrease size
        #  If the bucket does not contain the key, throw exception
        reference_list = self.table[index]

        # for i in range(len(reference_list)):
        #    package = reference_list[i]

        #    if package.get_id() == item:

        #        self.table.pop(i)
        #        self.size = self.size - 1
        #        return

        j = 0
        probe_index = index
        while j < self.listSize:
            # probe_index = probe_index + 1
            probe_index = probe_index + j * j
            while probe_index >= self.listSize:
                probe_index = probe_index - self.listSize

            reference_list = self.table[probe_index]

            for i in range(len(reference_list)):
                package = reference_list[i]

                if package.get_id() == item:
                    self.table.pop(item)
                    self.size = self.size - 1
                    return

            # if probe_index >= self.listSize:
            #    probe_index = probe_index - self.listSize
            #    reference_list = self.table[probe_index]

            #    for i in range(len(reference_list)):
            #        package = reference_list[i]

            #        if package.get_id() == item:

            #            self.table.pop(item)
            #            self.size = self.size - 1
            #            return

            j = j + 1

        raise RuntimeError("Item not found!")

    def hash(self, package_id):
        # TODO: How to determine a hash function for the insert, search, delete functions
        # Determine a unique key, probably the unique ID and weight combined
        if isinstance(package_id, int):
            key = package_id
        else:
            key = package_id.get_id()

        # Use the ID and weight as input to create unique hashes, need a good algorithm here
        if self.listSize >= key:
            hash_code = self.listSize % key
        else:
            hash_code = key % self.listSize
        return hash_code

    def reHash(self):
        # Swap out existing table and create a new one
        newTable = []
        oldTable = self.table

        # Increase the list size and populate the new table
        self.listSize = self.listSize * 2
        i = 0
        while i < self.listSize:
            newTable.append([])
            i = i + 1

        # Put new table in place
        self.table = newTable
        self.size = 0

        # Iterate over the old table and re-insert the items into the new table.
        for i in range(len(oldTable)):
            if len(oldTable[i]) > 0:
                for j in range(len(oldTable[i])):
                    same_item = oldTable[i][j]
                    if same_item is not None:
                        self.insert(same_item.get_id(), same_item)

