import linked_list


class MapGraph:
    adj_list = []

    def __init__(self):
        self.size = 0

    def insert_vertex(self, vertex):
        # Insert a vertex into the adjacency list.  The vertex will be the first item in the adjacency list.
        self.adj_list.append(linked_list.LinkedList())
        item_list = self.adj_list[vertex.get_id() - 1]
        item_list.insert(vertex, 0)
        self.size = self.size + 1

    def insert_edge(self, vertex, edge, distance):
        # Insert an edge into the adjacency list for the designated vertex, edge should include a distance value.
        index = vertex.get_id() - 1
        index2 = edge.get_id() - 1

        list = self.adj_list[index]
        list2 = self.adj_list[index2]

        if not list.contains(edge):
            list.insert(edge, distance)

        if not list2.contains(vertex):
            list2.insert(vertex, distance)

    def get_vertex(self, id):
        return self.adj_list[id - 1]
