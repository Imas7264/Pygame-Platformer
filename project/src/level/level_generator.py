import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE

WIDTH = WINDOW_WIDTH // TILE_SIZE
HEIGHT = WINDOW_HEIGHT // TILE_SIZE

def generate_level(level_number = 1):
 level = []

 #Boundary generation
 for row in range(HEIGHT):
  if row == 0 or row == HEIGHT-1:
   level.append("#" * WIDTH)
  else:
   level.append("#" + (" " * (WIDTH-2)) + "#")

 level = [list(row) for row in level]

 player_x, player_y = HEIGHT - 3, 2
 level[player_x][player_y] = "P"

 floor_row = HEIGHT - 2
 for col in range(1, WIDTH - 1):
  level[floor_row][col] = "G"

 #Platform generation
 platform_count = random.randint(5, 8)

 for _ in range(platform_count):
  platform_length = random.randint(2,6)
  platform_x = random.randint(1, WIDTH-platform_length-1)
  platform_y = random.randint(3, HEIGHT-3)
  
  for i in range(platform_length):
   level[platform_y][platform_x + i] = "G"

 #Enemy generation
 enemy_count = random.randint(platform_count-2, platform_count+2)


 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level