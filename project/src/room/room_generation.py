from pygame import Rect
import math
import random
from typing import Tuple

class Room:

    def __init__(self, x, y, width, height):
        # actual pygame room object
        self.rect = Rect((x, y), (width, height))
        self.color = "blue"

    @property
    def center(self):
        return (self.rect.centerx, self.rect.centery)


def generate_rooms(
		n: int,
        circle_center: Tuple[int, int],
        circle_radius: int,
        min_size: int,
        max_size: int
):
    rooms = []
    for _ in range(n):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)

        # polar coordinates
        # r = circle_radius * math.sqrt(random.random())
        r = circle_radius * math.pow(random.random(), 2)
        theta = random.uniform(0, 2 * math.pi)

        """
        - for simpler usecase use uniform distribution
        >>> r = circle_radius * random.random()

        - but this one makes much more sense if we want to cluster the
        rectangles near center
        >>> r = circle_radius * math.pow(random.random(), 2)
        """

        x = int(circle_center[0] + r * math.cos(theta) - w / 2)
        y = int(circle_center[1] + r * math.sin(theta) - h / 2)

        rooms.append(Room(x, y, w, h))

    return rooms

