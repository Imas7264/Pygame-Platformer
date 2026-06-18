import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 720
TILE_SIZE = 30
FPS = 40
# ANIMATION_SPEED = 6

#layers
Z_LAYERS = {
 "bg": 0,
 "terrain": 1,
 "player": 2
}