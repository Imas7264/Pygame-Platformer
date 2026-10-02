from scipy.spatial import Delaunay
import pygame

def compute_delaunay(rooms):
    if len(rooms) < 3:
        return []

    points = [room.center for room in rooms]
    tri = Delaunay(points)

    edges = set()

    for simplex in tri.simplices:
        for i in range(3):
            p1 = tuple(points[simplex[i]])
            p2 = tuple(points[simplex[(i + 1) % 3]])
            edge = tuple(sorted([p1, p2]))
            edges.add(edge)

    return list(edges)

