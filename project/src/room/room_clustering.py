import pygame


def squeeze_main_rooms(main_rooms, iterations=40, pull_speed=1, safe_gap=8):
    """Pulls filtered main rooms closer to their collective center

    into a tight cluster, maintaining a safe gap so they don't touch.
    """
    if not main_rooms:
        return

    for _ in range(iterations):
        # 1. Calculate the centroid (center of mass) of all main rooms
        total_x = sum(room.rect.centerx for room in main_rooms)
        total_y = sum(room.rect.centery for room in main_rooms)
        centroid = pygame.math.Vector2(
            total_x / len(main_rooms), total_y / len(main_rooms)
        )

        # 2. Move each room slightly toward the centroid and back up old positions
        moved_data = []
        for room in main_rooms:
            c = pygame.math.Vector2(room.rect.center)
            direction = centroid - c
            if direction.length_squared() > 1:
                direction = direction.normalize()
                orig_rect = room.rect.copy()
                room.rect.x += int(direction.x * pull_speed)
                room.rect.y += int(direction.y * pull_speed)
                moved_data.append((room, orig_rect))

        # 3. Check for close proximity/collisions using an expanded buffer
        collision_detected = False
        for i in range(len(main_rooms)):
            # Inflate rectangle by safe_gap to maintain distance
            r1_inflated = main_rooms[i].rect.inflate(safe_gap, safe_gap)
            for j in range(i + 1, len(main_rooms)):
                r2_inflated = main_rooms[j].rect.inflate(safe_gap, safe_gap)
                if r1_inflated.colliderect(r2_inflated):
                    collision_detected = True
                    break
            if collision_detected:
                break

        # If rooms get too close, revert this step's movement and stop squeezing
        if collision_detected:
            for room, orig_rect in moved_data:
                room.rect = orig_rect
            break
