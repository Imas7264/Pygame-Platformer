import pygame
import random
from pathfinder.graph import LevelGraph
from settings import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    TILE_SIZE,
    SPEED,
    JUMP_STRENGTH,
    GRAVITY,
)

WIDTH = WINDOW_WIDTH // TILE_SIZE
HEIGHT = WINDOW_HEIGHT // TILE_SIZE
BOUND_X = 1
BOUND_Y_UPPER = 2
BOUND_Y_LOWER = 1


def create_platform(x, y, length, level):
    for i in range(length):
        level[y][x + i] = "G"

    return level


def store_platform(x, y, length, connected, graph):
    n1 = graph.create_node((x, y - 1)).index

    if length == 1:
        n2 = n1
    else:
        n2 = graph.create_node((x + length - 1, y - 1)).index

    platform = {
        "x": x,
        "y": y,
        "length": length,
        "connected": connected,  # No. of plaforms reachable from this platform <max=2>
        "bound_x": (x - BOUND_X, x + length),  # Boundary for x coordinate
        "bound_y": (y + BOUND_Y_LOWER, y - BOUND_Y_UPPER),  # Boundary for y coordinate
        "left_node": n1,
        "right_node": n2,
    }

    return platform


def valid_platform(x, y, length, platforms) -> bool:
    for platform in platforms:
        if (
            (x + length - 1 >= platform["bound_x"][0] and x <= platform["bound_x"][1])
            and (y <= platform["bound_y"][0] and y >= platform["bound_y"][1])
        ) or (
            (
                platform["x"] + platform["length"] - 1 >= x - BOUND_X
                and platform["x"] <= x + length
            )
            and (
                platform["y"] <= y + BOUND_Y_LOWER
                and platform["y"] >= y - BOUND_Y_UPPER
            )
        ):
            return False

    return True


def create_landing_nodes_and_edges(platforms, graph, level):
    for platform in platforms:
        node = graph.get_node_by_id(platform["left_node"])
        x = node["pos"][0] - 1

        for y in range(node["pos"][1] + 1, HEIGHT):
            if level[y][x] == "G":
                if not graph.node_exists((x, y - 1)):
                    landing_node = graph.create_node((x, y - 1))
                else:
                    landing_node = graph.get_node_by_pos((x, y - 1))

                bidirectional = abs(y - node["pos"][1]) <= 4
                graph.create_edge(node.index, landing_node.index, bidirectional)
                break

        node = graph.get_node_by_id(platform["right_node"])
        x = node["pos"][0] + 1

        for y in range(node["pos"][1] + 1, HEIGHT):
            if level[y][x] == "G":
                if not graph.node_exists((x, y - 1)):
                    landing_node = graph.create_node((x, y - 1))
                else:
                    landing_node = graph.get_node_by_pos((x, y - 1))

                bidirectional = abs(y - node["pos"][1]) <= 4
                graph.create_edge(node.index, landing_node.index, bidirectional)
                break


def create_platform_edges(platforms, graph):
    for platform in platforms:
        node_index = platform["left_node"]
        y = platform["y"] - 1
        for x in range(platform["x"] + 1, platform["x"] + platform["length"]):
            if graph.node_exists((x, y)):
                temp = graph.get_node_by_pos((x, y))
                graph.create_edge(node_index, temp.index)
                node = temp


def populate_container():
    level = []
    graph = LevelGraph()

    # Boundary generation
    for row in range(HEIGHT):
        if row == 0 or row == HEIGHT - 1:
            level.append("#" * WIDTH)
        else:
            level.append("#" + (" " * (WIDTH - 2)) + "#")

    level = [list(row) for row in level]

    player_x, player_y = WIDTH // 3, HEIGHT // 2
    level[player_y][player_x] = "P"

    floor_row = player_y + 2
    floor_length = 4
    level = create_platform(player_x, floor_row, floor_length, level)

    # Platform generation
    platform = store_platform(player_x, floor_row, floor_length, 0, graph)
    platforms = [
        platform,
    ]
    active_platforms = [
        platform,
    ]

    platform_count = random.randint(8, 12)

    attempts = 0
    while len(platforms) <= platform_count - 1 and attempts <= 100:
        attempts += 1

        dx = random.choice([-4, -3, -2, 2, 3, 4])
        dy = random.randint(-2, 2)
        platform_length = random.randint(1, 4)

        parent = random.choice(active_platforms)

        if dx < 0:
            new_x = parent["x"] + dx - platform_length
        else:
            new_x = parent["x"] + dx + parent["length"]

        new_y = parent["y"] + dy

        if new_x < 2 or new_x + platform_length > WIDTH - 2:
            continue

        if new_y < 2 or new_y > HEIGHT - 2:
            continue

        if valid_platform(new_x, new_y, platform_length, platforms):
            level = create_platform(new_x, new_y, platform_length, level)

            platform = store_platform(new_x, new_y, platform_length, 0, graph)
            platforms.append(platform)

            active_platforms.append(platform)
            parent["connected"] += 1

            if parent["connected"] == 2:
                active_platforms.remove(parent)
        else:
            continue

    create_landing_nodes_and_edges(platforms, graph, level)
    create_platform_edges(platforms, graph)
    level = mark_nodes(graph, level)

    print("Total platforms: ", platform_count)
    print("Total attempts: ", attempts)

    print("Total nodes: ", graph.graph.vcount())
    print("Total edges: ", graph.graph.ecount())

    level = ["".join(row) for row in level]

    return level, graph


def mark_nodes(graph, level):
    for node in graph.get_nodes():
        pos = node["pos"]
        level[pos[1]][pos[0]] = "M"
        level[pos[1]][pos[0]] = "M"

    return level


def draw_edges(screen, graph):
    for edge in graph.get_edges():
        source = graph.get_node_by_id(edge.source)
        destination = graph.get_node_by_id(edge.target)

        source_pos = (
            source["pos"][0] * TILE_SIZE + TILE_SIZE // 2,
            source["pos"][1] * TILE_SIZE + TILE_SIZE // 2,
        )

        destination_pos = (
            destination["pos"][0] * TILE_SIZE + TILE_SIZE // 2,
            destination["pos"][1] * TILE_SIZE + TILE_SIZE // 2,
        )

        pygame.draw.line(screen, (255, 0, 0), source_pos, destination_pos, 2)
