import pygame
from pygame.math import Vector2

def get_distance(pos_a, pos_b):
  return pos_a.distance_to(pos_b)

def get_distance_vector(pos_a, pos_b):
  return Vector2(abs(pos_b.x-pos_a.x), abs(pos_b.y-pos_a.y))

def get_direction_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)

def add_vectors(vec_1, vec_2):
  return vec_1 + vec_2

def bounds_distance_vector(obj, oth):
  sbbx = obj.bounding_box.x
  sbby = obj.bounding_box.y
  srect_min_x = obj.pos.x - sbbx
  srect_max_x = obj.pos.x + sbbx
  srect_min_y = obj.pos.y - sbby
  srect_max_y = obj.pos.y + sbby
  obbx = oth.bounding_box.x
  obby = oth.bounding_box.y
  orect_min_x = oth.pos.x - obbx
  orect_max_x = oth.pos.x + obbx
  orect_min_y = oth.pos.y - obby
  orect_max_y = oth.pos.y + obby
  dx = max(srect_min_x - orect_min_x, 0, orect_max_x - srect_max_x)
  dy = max(srect_min_y - orect_min_y, 0, orect_max_y - srect_max_y)
  return Vector2(dx, dy)