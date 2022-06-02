import numpy as np
import math
from pygame.math import Vector2

bit_dict = {
  0: { 'character': ' ', 'offset': Vector2(0, 0)},
  1: { 'character': 'o', 'offset': Vector2(4, 4)},
  2: { 'character': 'O', 'offset': Vector2(2, 2)},
  3: { 'character': '0', 'offset': Vector2(0, 0)},
  4: { 'character': '@', 'offset': Vector2(0, 0)},
  5: { 'character': '*', 'offset': Vector2(0, 0)},
  6: { 'character': '-', 'offset': Vector2(0, 0)},
  7: { 'character': '.', 'offset': Vector2(0, 0)}
}

def read_bitval(index):
  return bit_dict[index]

def pos_to_pixpos(pos, cell_size):
  return Vector2(pos.x * cell_size, pos.y * cell_size)

def blank_bitmap(rows, columns):
  btmp = []
  for y in range(rows):
    bits = []
    for x in range(columns):
      bits.append(0)
    btmp.append(bits)
  return np.array(btmp)

def apply_border_threshold(width, height, border_width, pos):
  if pos.y <= border_width:
    pos.y = border_width
  if pos.y >= height-border_width:
    pos.y = height-border_width
  if pos.x >= width-border_width:
    pos.x = width-border_width
  if pos.x <= border_width:
    pos.x = border_width
  return pos


def update_bitmap(bitmap, cursor_border, objs_in_scene):
  y = len(bitmap)
  x = len(bitmap[0])
  for obj in objs_in_scene:
    obj.update()
    bit_pos = obj.pos
    bit_pos = apply_border_threshold(x, y, cursor_border, bit_pos)
    bitmap[int(bit_pos.y), int(bit_pos.x)] = obj.char_index
  return bitmap

def int_vector(vec):
  return Vector2(int(vec.x), int(vec.y))

def collision_to_vec(cm):
  d = Vector2(0, 0)
  for i, y in enumerate(cm):
    for j, x in enumerate(y):
      if x == 1:
        d = Vector2(d.x - (j-1), d.y - (i-1))
  if d.length() > 0:
    return d.normalize()
  else:
    return Vector2(0,0)

def collision_to_move(cm):
  if cm[1,0] == 0:
    return Vector2(-1, 0)
  elif cm[1,2] == 0:
    return Vector2(1, 0)
  elif cm[0, 1] == 0:
    return Vector2(0, -1)
  elif cm[2, 1] == 0:
    return Vector2(0, 1)
  else:
    return Vector2(0,0)
