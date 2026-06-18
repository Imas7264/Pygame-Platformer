import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE

WIDTH = WINDOW_WIDTH // TILE_SIZE
HEIGHT = WINDOW_HEIGHT // TILE_SIZE

def generate_level_random(level_number = 1):
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

 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level


def generate_level_path():
 level = []

 #Boundary generation
 for row in range(HEIGHT):
  if row == 0 or row == HEIGHT-1:
   level.append("#" * WIDTH)
  else:
   level.append("#" + (" " * (WIDTH-2)) + "#")

 level = [list(row) for row in level]

 player_x, player_y = 2, HEIGHT - 5
 level[player_y][player_x] = "P"

 floor_row = player_y + 2
 floor_length = 4
 for col in range(player_x, player_x+floor_length):
  level[floor_row][col] = "G"

 #Platform generation
 platform_count = random.randint(5, 12)
 current_x = player_x
 current_y = player_y+2
 current_length = floor_length

 for _ in range(platform_count):
  dx = random.randint(2,4)
  dy = random.randint(-2,2)

  platform_length = random.randint(1,4)
  platform_x = current_x + dx + current_length
  platform_y = current_y + dy

  platform_y = max(3, min(HEIGHT-5, platform_y))

  if(platform_x + platform_length) > WIDTH-2:
   break
  
  for i in range(platform_length):
   level[platform_y][platform_x + i] = "G"

  current_x = platform_x
  current_y = platform_y
  current_length = platform_length

 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level


def generate_network_level():
 level = []

 #Boundary generation
 for row in range(HEIGHT):
  if row == 0 or row == HEIGHT-1:
   level.append("#" * WIDTH)
  else:
   level.append("#" + (" " * (WIDTH-2)) + "#")

 level = [list(row) for row in level]

 player_x, player_y = WIDTH//3, HEIGHT//2
 level[player_y][player_x] = "P"

 floor_row = player_y + 2
 floor_length = 4
 for col in range(player_x, player_x+floor_length):
  level[floor_row][col] = "G"

 #Platform generation
 active_platforms = [
  [player_x, floor_row, 3, 0], #(x, y, length, connected platforms<max=2>)
 ]

 platform_count = random.randint(8, 12)
 
 i=platform_count
 while i>0:
  dx = random.randint(2,4)
  dy = random.randint(-2,2)
  platform_length = random.randint(1,4)

  parent = random.choice(active_platforms)
  direction = random.choice(["left", "up", "right", "down"])
  
  if direction == "right":
   new_x = parent[0] + parent[2] + dx
   new_y = parent[1] + dy
  
  elif direction == "left":
   new_x = parent[0] - parent[2] - dx
   new_y = parent[1] + dy
  
  elif direction == "up":
   new_x = parent[0] + dx
   new_y = parent[1] + dy + 1
  
  elif direction == "down":
   new_x = parent[0] + dx
   new_y = parent[1] + dy - 2

  level = create_platform(new_x, new_y, platform_length, level)
  parent[3] += 1
  
  if parent[3] >=2:
   active_platforms.remove(parent)

  active_platforms.append([new_x, new_y, platform_length, 0])
  i -= 1

 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level


def create_platform(x, y, length, level):
 for i in range(length):
  level[y][x + i] = "G"

 return level