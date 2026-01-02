import pygame
from settings import vector

class Enemy(pygame.sprite.Sprite):
 def __init__(self, pos):
  super().__init__()
  
  self.image = pygame.Surface((18, 26))
  self.image.fill("red")
  self.rect = self.image.get_rect(topleft=pos)

  #physics
  self.direction = vector(-1,0)
  self.speed = 2
  self.gravity = 0.8
  self.on_ground = False


 def apply_gravity(self):
  self.direction.y += self.gravity
  self.rect.y += self.direction.y


 def move(self):
  self.rect.x += self.direction.x * self.speed


 def get_ahead_position(self):
  if self.direction.x > 0:
   x = self.rect.right + 1
  else:
   x = self.rect.left + 1

  y = self.rect.bottom + 1
  return x, y
 

 