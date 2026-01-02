import pygame

class AttackHitbox(pygame.sprite.Sprite):
 def __init__(self, pos, size, duration = 10):
  super().__init__()

  self.image = pygame.Surface(size)
  self.image.fill("yellow")
  self.rect= self.image.get_rect(topleft = pos)

  self.timer = duration

 
 def update(self):
  self.timer -= 1
  
  if self.timer <= 0:
   self.kill()