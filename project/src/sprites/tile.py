import pygame
from settings import TILE_SIZE


class CollisionTile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

        if type == "#":
            self.image.fill("darkblue")
        else:
            self.image.fill("green")

        self.rect = self.image.get_rect(topleft=pos)


class BackgroundTile(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)

        self.rect = self.image.get_rect(topleft=pos)
