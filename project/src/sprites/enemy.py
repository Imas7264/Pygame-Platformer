import pygame

class Enemy(pygame.sprite.Sprite):
 def __init__(self, pos):
  super().__init__()
  
  self.image = pygame.Surface((24, 32))
  self.image.fill("red")
  self.rect = self.image.get_rect(topleft=pos)