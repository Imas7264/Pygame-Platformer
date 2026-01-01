import pygame
from settings import TILE_SIZE
from sprites.tile import Tile
from sprites.player import Player
from sprites.enemy import Enemy

class Level:
 def __init__(self, layout):
  self.display_surface = pygame.display.get_surface()
  self.tiles = pygame.sprite.Group()
  self.enemies = pygame.sprite.Group()
  self.player = None

  self.build_level(layout)


 def build_level(self, layout):
  for row_index, row in enumerate(layout):
   for col_index, cell in enumerate(row):
    x = col_index * TILE_SIZE
    y = row_index * TILE_SIZE

    if cell == "#":
     self.tiles.add(Tile((x, y), cell))

    elif cell == "P":
     self.player = Player((x, y))
    
    elif cell == "E":
     self.enemies.add(Enemy((x, y)))
    
    elif cell == "G":
     self.tiles.add(Tile((x, y), cell))


 def run(self):
  self.tiles.draw(self.display_surface)

  if self.player:
   #horizontal
   self.player.get_input()
   self.player.move_x()
   self.horizontal_collision()

   #vertical
   self.player.on_ground = False
   self.player.apply_gravity()
   self.vertical_collision()

   self.display_surface.blit(self.player.image, self.player.rect)

  self.enemies.draw(self.display_surface)


 def vertical_collision(self):
  player = self.player
  
  for tile in self.tiles:
   if tile.rect.colliderect(player.rect):

    #falling
    if player.direction.y > 0:
     player.rect.bottom = tile.rect.top
     player.direction.y = 0
     self.player.on_ground = True

    #hitting ceiling
    elif player.direction.y < 0:
     player.rect.top = tile.rect.bottom
     player.direction.y = 0


 def horizontal_collision(self):
  player = self.player

  for tile in self.tiles:
   if tile.rect.colliderect(player.rect):
    
    #moving right
    if player.direction.x > 0:
     player.rect.right = tile.rect.left

    #moving left
    if player.direction.x < 0:
     player.rect.left = tile.rect.right