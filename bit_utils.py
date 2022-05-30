import numpy as np
from pygame.math import Vector2

bit_dict = {
  0: { 'character': ' ', 'bounding_box': Vector2(0,0), 'offset': Vector2(0, 0)},
  1: { 'character': 'o', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  2: { 'character': 'O', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  3: { 'character': '0', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  4: { 'character': '@', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  5: { 'character': '*', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  6: { 'character': '-', 'bounding_box': Vector2(1,1), 'offset': Vector2(0, 0)},
  7: { 'character': '.', 'bounding_box': Vector2(0.5,0.5), 'offset': Vector2(0, 0)}
}

def read_bitval(index):
  return bit_dict[index]

def pos_to_pixpos(pos, cell_size):
  return Vector2(pos.x * cell_size, pos.y * cell_size)

def refresh_bitmap(rows, columns):
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


def update_bitmap(bit_width, bit_height, cursor_border, objs_in_scene):
  bitmap = refresh_bitmap(bit_width, bit_height)
  for obj in objs_in_scene:
    obj.update()
    bit_pos = obj.pos
    bit_pos = apply_border_threshold(bit_width, bit_height, cursor_border, bit_pos)
    bitmap[int(bit_pos.y), int(bit_pos.x)] = obj.char_index
  return bitmap