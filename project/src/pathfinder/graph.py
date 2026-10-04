import igraph


class LevelGraph:
    def __init__(self):
        self.graph = igraph.Graph(directed=True)

    def create_node(self, pos):
        node = self.graph.add_vertex(pos=pos)
        return node.index

    def create_edge(self, source, destination, bidirectional=True):
        self.graph.add_edge(source, destination)

        if bidirectional:
            self.graph.add_edge(destination, source)

    def get_nodes(self):
        return self.graph.vs


# graph = LevelGraph()

# n1 = graph.create_node((10, 20))
# n2 = graph.create_node((10, 40))
# graph.create_edge(n1, n2)
# print(graph.graph.vcount())
# print(graph.graph.ecount())
