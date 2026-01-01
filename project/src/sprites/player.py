import pygame
from settings import vector

class Player(pygame.sprite.Sprite):
 def __init__(self, pos):
  super().__init__()
  
  self.image = pygame.Surface((18, 24))
  self.image.fill("dodgerblue")
  self.rect = self.image.get_rect(topleft=pos)

  #physics
  self.direction = vector(0,0)
  self.speed = 5
  self.gravity = 0.8
  self.jump_strength = -15
  self.on_ground = False


 def get_input(self):
  keys = pygame.key.get_pressed()

  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
   self.direction.x = 1
  elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
   self.direction.x = -1
  else:
   self.direction.x = 0

  if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
   self.direction.y = self.jump_strength
   # self.rect.y += self.direction.y
   self.on_ground = False


 # def jump(self):
 #  if self.on_ground:
 #   print("JUMP")
 #   self.direction.y = self.jump_strength
 #   self.on_ground = False


 def move_x(self):
  self.rect.x += self.direction.x * self.speed
 
 
 def apply_gravity(self):
  self.direction.y += self.gravity

  if self.direction.y < -12:
   self.direction.y = -12

  self.rect.y += self.direction.y






