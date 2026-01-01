import sys
import pygame
from settings import *
from level.level import Level
from level.level_data import LEVEL_0

class Game:
 def __init__(self):
  pygame.init()
  self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption("Code-Based Level")
  self.clock = pygame.time.Clock()

  self.level = Level(LEVEL_0)

 def run(self):
  while True:

   for event in pygame.event.get():
    if event.type == pygame.QUIT:
     pygame.quit()
     sys.exit()

    # if event.type == pygame.KEYDOWN:
    #  if event.key == pygame.K_SPACE:
    #   game.level.player.jump()

   self.screen.fill("black")
   self.level.run()
   pygame.display.update()
   self.clock.tick(FPS)

if __name__ == "__main__":
 game = Game()
 game.run()