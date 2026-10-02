import math
# from data_structure.disjoint_set import DisjointSet

def compute_mst(delaunay_edges):
    """Computes minimum spanning tree using Kruskal's algorithm."""

    edges_with_weights = []

    for edge in delaunay_edges:
        p1, p2 = edge

        dist = math.hypot(p2[0] - p1[0], p2[1] - p2[1])
        edges_with_weights.append((dist, p1, p2))

    # sort the edges according the weights
    # making it convenient to perform kruskal's algo

    edges_with_weights.sort(key=lambda x: x[0])

    parent = {}

    def find(i):
        if i == parent[i]:
            return i

        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        p_i = find(i)
        p_j = find(j)

        if p_i != p_j:
            parent[p_i] = p_j
            return True

        return False

    points = set()

    for _, p1, p2 in edges_with_weights:
        points.add(p1)
        points.add(p2)

    for p in points:
        parent[p] = p

    mst_edges = []

    for dist, p1, p2 in edges_with_weights:
        if union(p1, p2):
            mst_edges.append((p1, p2))


    return mst_edges

    

