import igraph


class LevelGraph:
    def __init__(self):
        self.graph = igraph.Graph(directed=True)

    def create_node(self, pos):
        node = self.graph.add_vertex(pos=pos)
        return node

    def create_edge(self, source, destination, bidirectional=True):
        self.graph.add_edge(source, destination)

        if bidirectional:
            self.graph.add_edge(destination, source)

    def get_nodes(self):
        return self.graph.vs

    def get_edges(self):
        return self.graph.es

    def node_exists(self, pos):
        return pos in self.graph.vs["pos"]

    def get_node_by_id(self, node_id):
        return self.graph.vs[node_id]

    def get_node_by_pos(self, pos):

        for node in self.graph.vs:
            if node["pos"] == pos:
                return node

        return None


# graph = LevelGraph()

# n1 = graph.create_node((10, 20))
# n2 = graph.create_node((10, 40))
# graph.create_edge(n1, n2)
# print(graph.graph.vcount())
# print(graph.graph.ecount())
