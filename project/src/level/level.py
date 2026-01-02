import pygame
from settings import TILE_SIZE
from sprites.tile import Tile
from sprites.player import Player
from sprites.enemy import Enemy
from sprites.attack import AttackHitbox

class Level:
 def __init__(self, layout):
  self.display_surface = pygame.display.get_surface()
  self.tiles = pygame.sprite.Group()
  self.enemies = pygame.sprite.Group()
  self.player = None
  self.attack_sprites = pygame.sprite.Group()

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

  #player
  if self.player:
   #horizontal
   self.player.get_input()
   self.player.move_x()
   self.horizontal_collision()

   #vertical
   self.player.on_ground = False
   self.player.apply_gravity()
   self.vertical_collision()

   self.player.update_attack()
   self.handle_player_attack()
   self.display_surface.blit(self.player.image, self.player.rect)

  #enemies
  for enemy in self.enemies:
   #edge detection and turning
   if enemy.on_ground and not self.enemy_has_ground_ahead(enemy):
    enemy.direction.x *= -1

   #horizontal
   enemy.move()
   self.enemy_horizontal_collision(enemy)

   #vertical
   enemy.on_ground = False
   enemy.apply_gravity()
   self.enemy_vertical_collision(enemy)

  #player hits enemy
  for hitbox in self.attack_sprites:
   for enemy in self.enemies:
    if hitbox.rect.colliderect(enemy.rect):
     print("Enemy hit!!!")
     hitbox.kill()
     break

  self.attack_sprites.update()
  self.attack_sprites.draw(self.display_surface)

  self.enemies.draw(self.display_surface)


 def vertical_collision(self):
  player = self.player
  
  for tile in self.tiles:
   if tile.rect.colliderect(player.rect):

    #landing
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


 def enemy_horizontal_collision(self, enemy):
  for tile in self.tiles:
   if tile.rect.colliderect(enemy.rect):
    #wall on right
    if enemy.direction.x > 0:
     enemy.rect.right = tile.rect.left
     enemy.direction.x *= -1

    #wall on left
    elif enemy.direction.x < 0:
     enemy.rect.left = tile.rect.right
     enemy.direction.x *= -1
   

 def enemy_vertical_collision(self, enemy):
  for tile in self.tiles:
   if tile.rect.colliderect(enemy.rect):
    #landing
    if enemy.direction.y > 0:
     enemy.rect.bottom = tile.rect.top
     enemy.direction.y = 0
     enemy.on_ground = True


 def enemy_has_ground_ahead(self, enemy):
   check_x, check_y = enemy.get_ahead_position()

   for tile in self.tiles:
    if tile.rect.collidepoint(check_x, check_y):
     return True
    
   return False
 

 def handle_player_attack(self):
  player = self.player

  if player.attacking:
   pos, size = player.create_attack_hitbox()
   hitbox = AttackHitbox(pos, size)
   self.attack_sprites.add(hitbox)
   player.attacking = False