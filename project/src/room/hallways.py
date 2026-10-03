import pygame


def generate_hallways(
    mst_edges, alignment_threshold=15, hallway_width=30
):  # hallway_width acts as the room size/thickness
    """Generates hallway line segments and converts them into thick rectangular room blocks."""
    hallway_rects = []

    for p1, p2 in mst_edges:
        x1, y1 = p1
        x2, y2 = p2

        # collect the individual line segments based on your alignment rules
        segments = []
        if abs(y1 - y2) <= alignment_threshold:
            segments.append((p1, (x2, y1)))
        elif abs(x1 - x2) <= alignment_threshold:
            segments.append((p1, (x1, y2)))
        else:
            corner = (x2, y1)
            segments.append((p1, corner))
            segments.append((corner, p2))

        # convert each line segment into a thick rectangular room block
        for seg_p1, seg_p2 in segments:
            sx1, sy1 = seg_p1
            sx2, sy2 = seg_p2

            x_min = min(sx1, sx2)
            x_max = max(sx1, sx2)
            y_min = min(sy1, sy2)
            y_max = max(sy1, sy2)

            # if it's a horizontal segment
            if y_min == y_max:
                rect = pygame.Rect(
                    x_min,
                    y_min - hallway_width // 2,
                    x_max - x_min,
                    hallway_width,
                )
            # if it's a vertical segment
            else:
                rect = pygame.Rect(
                    x_min - hallway_width // 2,
                    y_min,
                    hallway_width,
                    y_max - y_min,
                )

            hallway_rects.append(rect)

    return hallway_rects
