import pygame
from pygame.math import Vector2

def clip(val):
  return round(val, 2)

# def get_distance(pos_a, pos_b):
#   return pos_a.distance_to(pos_b)

# def get_distance_vector(pos_a, pos_b):
#   return Vector2(abs(pos_b.x-pos_a.x), abs(pos_b.y-pos_a.y))

def get_direction_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)

def get_midway_point(pos_a, pos_b):
  dvect = Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)
  return Vector2(clip(pos_a.x + dvect.x/2), clip(pos_a.y + dvect.y/2))


def get_normal(pos_a, pos_b):
  dv = get_direction_vector(pos_a, pos_b)
  if dv.length() > 0:
    norm = dv.normalize()
    return Vector2(clip(norm.x), clip(norm.y))
  else:
    return Vector2(0, 0)

def generate_bounds(obj):
  bbx = obj.bounding_box.x
  bby = obj.bounding_box.y
  rect_min_x = obj.pos.x - bbx
  rect_max_x = obj.pos.x + bbx
  rect_min_y = obj.pos.y - bby
  rect_max_y = obj.pos.y + bby
  return { 'leftX': rect_min_x, 'rightX': rect_max_x, 'topY': rect_min_y, 'bottomY': rect_max_y }

def bounds_collided(obj, oth):
  rect1 = generate_bounds(obj)
  rect2 = generate_bounds(oth)
  leftX = max(rect1['leftX'], rect2['leftX'])
  rightX = min(rect1['rightX'], rect2['rightX'])
  topY = max(rect1['topY'], rect2['topY'])
  bottomY = min(rect1['bottomY'], rect2['bottomY'])
  if leftX < rightX and topY < bottomY:
    return True
  else:
    return False