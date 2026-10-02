import sys
import pygame
from delaunay_graph import compute_delaunay
from hallways import generate_hallways
from mst_graph import compute_mst
from room_clustering import squeeze_main_rooms
from room_filtering import filter_main_rooms
from room_generation import generate_rooms
from room_separation import update_separation

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Dungeon Generator - Integrated Pipeline")
clock = pygame.time.Clock()

NUM_ROOMS = 60
CIRCLE_CENTER = (WIDTH // 2, HEIGHT // 2)
CIRCLE_RADIUS = 300
MIN_SIZE, MAX_SIZE = 40, 90
MIN_WIDTH_THRESH, MIN_HEIGHT_THRESH = 60, 60

# States:
# 1: Generate Rooms
# 2: Separating Rooms (Animation)
# 3: Separation Complete -> Filter Main Rooms & Squeeze
# 4: Delaunay Triangulation
# 5: Minimum Spanning Tree (MST)
# 6: Final Hallways & Dungeon Render
state = 1
rooms = generate_rooms(NUM_ROOMS, CIRCLE_CENTER, CIRCLE_RADIUS, MIN_SIZE, MAX_SIZE)
main_rooms = []
delaunay_edges = []
mst_edges = []
hallways = []

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == 1:
                    state = 2  # start separation animation
                elif state == 3:
                    # filter main rooms and immediately squeeze them closer together
                    main_rooms = filter_main_rooms(
                        rooms, MIN_WIDTH_THRESH, MIN_HEIGHT_THRESH
                    )
                    squeeze_main_rooms(main_rooms)
                    state = 4  # Move to Delaunay Triangulation
                elif state == 4:
                    delaunay_edges = compute_delaunay(main_rooms)
                    state = 5  # Compute MST
                elif state == 5:
                    mst_edges = compute_mst(delaunay_edges)
                    hallways = generate_hallways(mst_edges)
                    state = 6  # Final dungeon view
                elif state == 6:
                    # reset simulation data cache
                    rooms = generate_rooms(
                        NUM_ROOMS, CIRCLE_CENTER, CIRCLE_RADIUS, MIN_SIZE, MAX_SIZE
                    )
                    main_rooms = []
                    delaunay_edges = []
                    mst_edges = []
                    hallways = []
                    state = 1

    # separation
    if state == 2:
        is_fully_separated = update_separation(rooms)
        if is_fully_separated:
            state = 3

    pygame.draw.circle(screen, (50, 50, 50), CIRCLE_CENTER, CIRCLE_RADIUS, 2)

    # delaunay edges
    if state == 4:
        if not delaunay_edges and main_rooms:
            delaunay_edges = compute_delaunay(main_rooms)
        for edge in delaunay_edges:
            pygame.draw.line(screen, (100, 100, 100), edge[0], edge[1], 1)

    # generate mst
    if state == 5:
        if not mst_edges and delaunay_edges:
            mst_edges = compute_mst(delaunay_edges)
        for edge in mst_edges:
            pygame.draw.line(screen, (200, 150, 50), edge[0], edge[1], 2)

    # final hallway
    if state == 6:
        for hallway in hallways:
            pygame.draw.line(screen, (220, 220, 220), hallway[0], hallway[1], 4)

    # draw the rooms
    for room in rooms:
        if state >= 4 and room not in main_rooms:
            continue
        pygame.draw.rect(screen, room.color, room.rect)
        pygame.draw.rect(screen, (255, 255, 255), room.rect, 1)

    # intructions to be displayed on the game screen.
    font = pygame.font.SysFont(None, 24)
    instructions = {
        1: "Step 1: Rooms Generated. Press [SPACE] to start Separation Animation.",
        2: "Step 2: Separating Rooms (Watch animation)...",
        3: (
            "Step 3: Separation Complete. Press [SPACE] to Filter & Squeeze Main"
            " Rooms."
        ),
        4: "Step 4: Delaunay Triangulation Computed. Press [SPACE] to build MST.",
        5: "Step 5: MST Computed. Press [SPACE] to Generate Hallways.",
        6: (
            "Step 6: Final Dungeon Complete with Squeezed Rooms & Hallways! Press"
            " [SPACE] to Reset."
        ),
    }
    text_surface = font.render(instructions.get(state, ""), True, (255, 255, 255))
    screen.blit(text_surface, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
