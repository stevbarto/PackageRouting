class MapGraph:
    adj_matrix = []

    def __init__(self):
        self.size = 0

    def insert_vertex(self):
        # Insert a vertex into the adjacency matrix.
        self.adj_matrix.append([])
        self.size = self.size + 1

    def insert_edge(self, vertex, edge, distance):
        # Insert an edge into the adjacency matrx for the designated vertex, edge index in teh list will be the
        # distance.
        v_id = vertex.get_id() - 1
        e_id = edge.get_id() - 1
        row = self.adj_matrix[v_id]
        row.insert(e_id, distance)
        if v_id != e_id:
            row = self.adj_matrix[e_id]
            row.insert(v_id, distance)
        # row[e_id] = distance

    def get_vertex(self, id):
        return self.adj_matrix[id - 1][0]


