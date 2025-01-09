"""
With Sherry Bai and Eric Dalva!

For creative coding on 2025-01-08. The prompt was "Draw a million of something".

"""


from collections import deque
import sys
import random
import time

GRID_SIZE = 64

MOUNTAIN = "🗻"
HILL = "⛰️ "
LAND = "🌲"
WATER = "🌊"
DRAGON = "🐉"
HOLE = "O "
# grid is 128 x 128 chars
chars = [MOUNTAIN, HILL, LAND, WATER, DRAGON]

tile_to_probs = {
    MOUNTAIN: [0.8, 0.2, 0.1, 0.1, 0.001],
    HILL: [0.2, 0.8, 0.1, 0.1, 0.001],
    LAND: [0.1, 0.1, 0.7, 0.1, 0.001],
    WATER: [0.1, 0.1, 0.2, 0.8, 0.001],
    HOLE: [0, 0, 0, 0, 0],
    DRAGON: [0.8, 0.1, 0.1, 0.1, 0],
}


def gen_island():
  grid = [[HOLE] * GRID_SIZE for _ in range(GRID_SIZE)]
  grid[GRID_SIZE // 2][GRID_SIZE // 2] = MOUNTAIN
  return grid


grid = gen_island()


def print_island(grid):
  sys.stdout.write("\033[H")  # Move cursor to the top-left
  sys.stdout.write("\033[J")  # Clear the screen below the cursor
  for column in grid:
    for line in column:
      print(line, end="")
    print()
  time.sleep(0.01)
  sys.stdout.flush()


def update():
  # assign the center cell
  center_item = (GRID_SIZE // 2, GRID_SIZE // 2)
  update_queue = deque([center_item])
  for diffx, diffy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
    update_queue.append((center_item[0] + diffx, center_item[1] + diffy))

  while update_queue:
    current_x, current_y = update_queue.popleft()
    if grid[current_x][current_y] != HOLE:
      continue
    if (current_x >= 0 or current_x <= GRID_SIZE) and (current_y >= 0 or
                                                       current_y <= GRID_SIZE):
      probs_array = [0, 0, 0, 0, 0]
      # visit all the neighbors of the current cell
      for diffx, diffy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        x = current_x + diffx
        y = current_y + diffy
        if (x < 0 or x >= GRID_SIZE) or (y < 0 or y >= GRID_SIZE):
          continue
        vals = tile_to_probs[grid[x][y]]
        if grid[x][y] == HOLE:
          update_queue.append((x, y))
        for idx, val in enumerate(vals):
          probs_array[idx] += val  #sum probs for surrounding tile types
      norm = sum(probs_array)
      probs_array = [val / norm for val in probs_array]
      tile = random.choices(chars, probs_array)
      grid[current_x][current_y] = tile[0]
      print_island(grid)


update()

# print_island(grid)
