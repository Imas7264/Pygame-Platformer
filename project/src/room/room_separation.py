import pygame

def update_separation(rooms):
	"""returns `True` if all the rooms are separated."""

	separated = True

	n = len(rooms)
	for i in range(n):
		for j in range(i + 1, n):
			r1 = rooms[i]
			r2 = rooms[j]

			if r1.rect.colliderect(r2.rect):
				separated = False

				c1 = pygame.math.Vector2(r1.rect.center)
				c2 = pygame.math.Vector2(r2.rect.center)

				direction = c1 - c2

				if direction.length_squared() == 0:
					# direction.length would have made more sense
					direction = pygame.math.Vector2(1, 0)
				else:
					# converts to unit vector with same direction
					direction = direction.normalize()

				# push rooms slightly apart
				push_step = 2

				r1.rect.x += int(direction.x * push_step)
				r1.rect.y += int(direction.y * push_step)
				r2.rect.x -= int(direction.x * push_step)
				r2.rect.y -= int(direction.y * push_step)


	return separated
				
