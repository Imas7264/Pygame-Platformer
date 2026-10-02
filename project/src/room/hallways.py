def generate_hallways(mst_edges, alignment_threshold=15):
    """Generates hallway line segments based on room alignment (straight or L-shape)."""
    hallways = []
    for p1, p2 in mst_edges:
        x1, y1 = p1
        x2, y2 = p2

        # Check if horizontally close (similar y positions)
        if abs(y1 - y2) <= alignment_threshold:
            hallways.append((p1, (x2, y1)))
        # Check if vertically close (similar x positions)
        elif abs(x1 - x2) <= alignment_threshold:
            hallways.append((p1, (x1, y2)))
        else:
            # L-shape: Create a corner point and split into two segments
            corner = (x2, y1)
            hallways.append((p1, corner))
            hallways.append((corner, p2))

    return hallways
