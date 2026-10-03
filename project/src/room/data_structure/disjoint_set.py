class DisjointSet:

    def __init__(self, n):
        self.size = n
        self.parent = {i: i for i in range(n)}

    def find(self, i):
        """Returns the root parent of the node"""
        if i == self.parent[i]:
            return i

        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Connects two unconnected nodes. Returns True if were not connected intially, else False"""
        p_i = self.find(i)
        p_j = self.find(j)

        if p_i != p_j:
            self.parent[p_i] = j
            return True

        return False