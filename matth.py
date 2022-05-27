import pygame
from pygame.math import Vector2

def get_distance(pos_a, pos_b):
  return pos_a.distance_to(pos_b)

def get_distance_vector(pos_a, pos_b):
  return Vector2(abs(pos_b.x-pos_a.x), abs(pos_b.y-pos_a.y))

def get_direction_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x + 1, pos_b.y - pos_a.y + 1)

def add_vectors(vec_1, vec_2):
  return vec_1 + vec_2

def generate_bounds_rect(obj):
  bbx = obj.bounding_box.x
  bby = obj.bounding_box.y
  rect_min_x = obj.pos.x - bbx
  rect_min_y = obj.pos.y - bby
  return pygame.Rect((rect_min_x, rect_min_y), (bbx * 2, bby * 2))

def bounds_collided(obj, oth):
  rect1 = generate_bounds_rect(obj)
  rect2 = generate_bounds_rect(oth)
  return rect1.colliderect(rect2)

def get_collision_rect(obj, oth):
  r1 = generate_bounds_rect(obj)
  r2 = generate_bounds_rect(oth)
  leftX = max(r1.left, r2.left)
  rightX = min(r1.right + obj.bounding_box.x, r2.right + oth.bounding_box.x)
  topY = max(r1.top, r2.top)
  bottomY = min(r1.bottom + obj.bounding_box.y, r2.bottom + oth.bounding_box.y)
  if leftX < rightX and topY < bottomY:
    width = rightX-leftX
    height = bottomY-topY
    return pygame.Rect(leftX, topY, width, height)
  else:
    return None