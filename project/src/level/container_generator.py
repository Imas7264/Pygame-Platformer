import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE, SPEED, JUMP_STRENGTH, GRAVITY

WIDTH = WINDOW_WIDTH // TILE_SIZE
HEIGHT = WINDOW_HEIGHT // TILE_SIZE


def create_platform(x, y, length, level):
 for i in range(length):
  level[y][x + i] = "G"

 return level


def store_platform(x, y, length, connected):
 platform = {
  "plat_x": x,
  "plat_y": y,
  "length": length,
  "connected": connected,         # No. of plaforms reachable from this platform <max=2>
  "bound_x": (x-1, x+length),     # Boundary for x coordinate
  "bound_y": (y+2, y-3)           # Boundary for y coordinate
 }

 return platform


def valid_platform(x, y, length, platforms)  -> bool:
 for platform in platforms:
  if (
      (
       x+length-1>=platform["bound_x"][0] and
       x<=platform["bound_x"][1]
      ) 
       and 
      (
       y<=platform["bound_y"][0] and
       y>=platform["bound_y"][1]
      )
     ):
   return False

 return True


def populate_container():
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
 level = create_platform(player_x, floor_row, floor_length, level)

 #Platform generation
 platform = store_platform(player_x, floor_row, floor_length, 0)
 platforms = [platform,]
 active_platforms = [platform,]

 platform_count = random.randint(8, 12)

 attempts=0
 while len(platforms) <= platform_count-1 and attempts <= 100:
  attempts+=1

  dx = random.choice([-4, -3, -2, 2, 3, 4])
  dy = random.randint(-2,2)
  platform_length = random.randint(1,4)

  parent = random.choice(active_platforms)
  
  if dx<0:
   new_x = parent["plat_x"] + dx - platform_length
  else:
   new_x = parent["plat_x"] + dx + parent["length"]

  new_y = parent["plat_y"] + dy

  if new_x < 2 or new_x+platform_length > WIDTH-2:
   continue
  
  if new_y < 2 or new_y > HEIGHT-2:
   continue

  if valid_platform(new_x, new_y, platform_length, platforms):
   level = create_platform(new_x, new_y, platform_length, level)
   
   platform = store_platform(new_x, new_y, platform_length, 0)
   platforms.append(platform)

   active_platforms.append(platform)
   parent["connected"] += 1

   if parent["connected"] == 2:
    active_platforms.remove(parent)
  else: 
   continue

 print("Total platforms: ", platform_count)
 print("Total attempts: ", attempts)
 level = ["".join(row) for row in level]

 return level