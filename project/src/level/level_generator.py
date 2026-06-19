import random
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, TILE_SIZE, SPEED, JUMP_STRENGTH, GRAVITY

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


def generate_level_network():
 level = []

 #Boundary generation
 for row in range(HEIGHT):
  if row == 0 or row == HEIGHT-1:
   level.append("#" * WIDTH)
  else:
   level.append("#" + (" " * (WIDTH-2)) + "#")

 level = [list(row) for row in level]

 player_x, player_y = WIDTH//3, HEIGHT//2

 floor_row = player_y + 2
 floor_length = 4
 level = create_platform(player_x, floor_row, floor_length, level)

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

 level[player_y][player_x] = "P"

 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level


def generate_level_arena():
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
 active_platforms = [
  (player_x, floor_row, floor_length), #(x, y, length, connected platforms<max=2>)
 ]

 platform_count = random.randint(8, 12)

 attempts=0
 while len(active_platforms) <= platform_count and attempts <= 100:
  attempts+=1

  dx = random.choice([-4, -3, -2, 2, 3, 4])
  dy = random.randint(-2,2)
  platform_length = random.randint(1,4)

  parent = random.choice(active_platforms)
  
  if dx<0:
   new_x = parent[0] + dx - platform_length
  else:
   new_x = parent[0] + dx + parent[2]

  new_y = parent[1] + dy  

  if new_x < 2 or new_x+platform_length > WIDTH-2:
   continue
  
  if new_y < 2 or new_y > HEIGHT-2:
   continue
  
  level = create_platform(new_x, new_y, platform_length, level)
  
  active_platforms.append((new_x, new_y, platform_length))

 print("Total platforms: ", platform_count)
 level = ["".join(row) for row in level]

 return level


def generate_level_full(seed=None):
 """
 Fill the entire screen with platforms that are guaranteed reachable.

 Strategy
 ────────
 1.  Place a starting platform near the bottom-left and put the player
     on it.
 2.  Divide the playable area into a grid of (band  zone) cells —
     horizontal bands of BAND_H rows, vertical zones of ZONE_W cols.
 3.  For every cell, attempt up to MAX_ATTEMPTS random platforms.
     Accept the first one that is reachable from ANY already-placed
     platform.  This ensures connectivity by construction.
 4.  The reachability test uses the exact same frame-by-frame physics
     as the actual player, so nothing placed here is theoretically
     impossible to reach.
 """
 if seed is not None:
     random.seed(seed)

 #Boundary generation
 level = []

 for row in range(HEIGHT):
  if row == 0 or row == HEIGHT-1:
   level.append("#" * WIDTH)
  else:
   level.append("#" + (" " * (WIDTH-2)) + "#")

 level = [list(row) for row in level]

 s_col = random.randint(2, 6)
 s_row = HEIGHT - 4
 s_length = random.randint(1, 3)
 level = create_platform(s_col, s_row, s_length, level)

 player_row = s_row - 1      # one tile above the starting platform
 player_col = s_col + 1      # second tile in from the left edge

 placed = [(s_col, s_row, s_length)]         # list of (x, y, length) tuples

 # ── band / zone pass ─────────────────────────────────────────────────
 BAND_H       = 4    # rows per horizontal band
 ZONE_W       = 6    # cols per vertical zone
 MIN_LEN      = 2    # shortest platform in tiles
 MAX_LEN      = 4    # longest platform in tiles
 MAX_ATTEMPTS = 500   # retries per cell before giving up

 for band_top in range(2, HEIGHT - 3, BAND_H):
  for zone_left in range(1, WIDTH - 2, ZONE_W):
   for _ in range(MAX_ATTEMPTS):

    pl = random.randint(MIN_LEN, MAX_LEN)
    
    # Random column within zone, clamped to playable area
    px = zone_left + random.randint(0, max(0, ZONE_W - pl - 1))
    py = band_top  + random.randint(0, BAND_H - 1)
    px = max(1, min(WIDTH - 2 - pl, px))
    py = max(2, min(HEIGHT - 3,    py))

    if any(can_reach(ep, (px, py, pl)) for ep in placed):
     for c in range(px, px + pl):
      level[py][c] = "G"
     placed.append((px, py, pl))
     break   # move on to the next cell

 level[player_row][player_col] = "P"

 return ["".join(row) for row in level]


def create_platform(x, y, length, level):
 for i in range(length):
  level[y][x + i] = "G"

 return level


def jump_reach(dy):
 if dy<0:
  rise_px = -dy*TILE_SIZE
  vy, x, y = float(JUMP_STRENGTH), 0.0, 0.0
  last_x = 0.0

  for _ in range(300):
   vy += GRAVITY
   x += SPEED
   y += vy

   if y <= -rise_px:
    last_x = x

   if y > 0:
    break

  return last_x / TILE_SIZE
 
 else:
  drop_px = dy * TILE_SIZE

  if drop_px == 0:
   vy, x, y = float(JUMP_STRENGTH), 0.0, 0.0
   for _ in range(300):
    vy += GRAVITY
    x += SPEED
    y += vy

    if y>=0 and _>3:
     break

   return x/TILE_SIZE
 
  t = (2*drop_px/GRAVITY)**0.5
  return (SPEED*t)/TILE_SIZE


def can_reach(p1, p2):
 dy = p2[1] - p1[1]
 max_gap = jump_reach(dy)

 p1_left = p1[0]
 p1_right = p1[0]+p1[2]-1
 p2_left = p2[0]
 p2_right = p2[0]+p2[2]-1

 gap_right = p2_left - p1_right - 1
 if 0 <= gap_right <= max_gap:
  return True
 
 gap_left = p1_left - p2_right - 1
 if 0 <= gap_left <= max_gap:
  return True
 
 if not (p2_right<p1_left or p2_left>p1_right):
  return True
 
 return False