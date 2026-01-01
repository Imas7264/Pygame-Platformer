import pygame
from settings import TILE_SIZE

class Tile(pygame.sprite.Sprite):
 def __init__(self, pos, type):
  super().__init__()
  if type == '#':
   self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
   self.image.fill("darkblue")
   self.rect = self.image.get_rect(topleft=pos)
  else:
   self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
   self.image.fill("green")
   self.rect = self.image.get_rect(topleft=pos)
   