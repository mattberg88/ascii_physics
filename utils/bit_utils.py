import numpy as np
import math
from pygame.math import Vector2

def speed_to_char(speed_vector):
  x,y = speed_vector.x, speed_vector.y
  if (x > 0.5 and y > 0.5) or (x < -0.5 and y < -0.5): return 12
  if (x < -0.5 and y > 0.5) or (x > 0.5 and y < -0.5 ): return 11
  if abs(x) > 0.5 : return 3
  if abs(y) > 0.5 : return 8
  else: return 1

def vector_mult(pos_a, pos_b):
  return Vector2(pos_a.x * pos_b.x, pos_a.y * pos_b.y)

def get_distance_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)

def apply_border_threshold(width, height, border_width, pos):
  p = Vector2(pos.x, pos.y)
  if p.y <= border_width:
    p.y = border_width
  if p.y >= height-border_width:
    p.y = height-border_width
  if p.x >= width-border_width:
    p.x = width-border_width
  if p.x <= border_width:
    p.x = border_width
  return p

def is_oob(width, height, border_width, pos):
  p = Vector2(pos.x, pos.y)
  if p.y <= border_width:
    return True
  if p.y >= height-border_width:
    return True
  if p.x >= width-border_width:
    return True
  if p.x <= border_width:
    return True
  return False

def update_bitmap(bit_width, bit_height, border_width, objs_in_scene):
  bit_array = []
  for y in range(bit_height):
    bits = []
    for x in range(bit_width):
      bits.append(0)
    bit_array.append(bits)
  bitmap = np.array(bit_array)
  y = len(bitmap)
  x = len(bitmap[0])
  for obj in objs_in_scene:
    obj.update()
    bit_pos = obj.pos
    bit_pos = apply_border_threshold(x, y, border_width, bit_pos)
    bitmap[int(bit_pos.y), int(bit_pos.x)] = obj.id
  return bitmap

def limit_vector(vec, limit):
  v = vec
  if v.x > limit:
    v.x = limit
  if v.x < -limit:
    v.x = -limit
  if v.y > limit:
    v.y = limit
  if v.y < -limit:
    v.y = -limit
  return v

def animate_chara(width, height, pos):
  x, y = pos[0], pos[1]
  if x == width/2 and y == height: return 0
  if x>width/2 and y>height - height/5: return 1
  if x<width/2 and y>height - height/5: return 5
  if x>width/2 and y>height/3: return 2
  if x<width/2 and y>height/3: return 4
  if x == width/2 and y<height/2: return 3
  return 0

def int_vector(vec):
  return Vector2(int(vec.x), int(vec.y))

def round_vector(vec, factor=5):
  return Vector2(round(vec.x, factor), round(vec.y, factor))

def bitmap_to_cm(bitmap, pos):
  center = bitmap[int(pos.y), int(pos.x)]
  top = bitmap[int(pos.y - 1), int(pos.x)]
  bottom = bitmap[int(pos.y + 1), int(pos.x)]
  left = bitmap[int(pos.y), int(pos.x - 1)]
  right = bitmap[int(pos.y), int(pos.x + 1)]
  l_top = bitmap[int(pos.y - 1), int(pos.x - 1)]
  r_top = bitmap[int(pos.y - 1), int(pos.x + 1)]
  l_bottom = bitmap[int(pos.y + 1), int(pos.x - 1)]
  r_bottom = bitmap[int(pos.y + 1), int(pos.x + 1)]
  return np.array([[l_top,top,r_top], [left,center,right], [l_bottom,bottom,r_bottom]])

def collision_to_vec(cm):
  d = Vector2(0, 0)
  for i, y in enumerate(cm):
    for j, x in enumerate(y):
      if x != 0:
        d = Vector2(d.x - (j-1), d.y - (i-1))
  if d.length() > 0:
    return d.normalize()
  else:
    return Vector2(0, 0)

def collision_to_move(cm):
  if cm[0, 1] == 0:
    return Vector2(0, -1)
  elif cm[1,0] == 0:
    return Vector2(-1, 0)
  elif cm[1,2] == 0:
    return Vector2(1, 0)
  elif cm[2, 1] == 0:
    return Vector2(0, 1)
  else:
    return Vector2(0, 0)

