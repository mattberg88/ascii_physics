import pygame
import math
from pygame.math import Vector2

def calculateDistance(pos_a, pos_b):
  dist = math.sqrt((pos_b.x - pos_a.x)**2 + (pos_b.y - pos_a.y)**2)
  return dist

def vector_mult(pos_a, pos_b):
  return Vector2(round(pos_a.x * pos_b.x, 2), round(pos_a.y * pos_b.y, 2))

def get_midpoint_vector(pos_a, pos_b):
  return Vector2((pos_b.x - pos_a.x)/2, (pos_b.y - pos_a.y)/2)


def get_distance_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)

def get_direction_norm(pos_a, pos_b):
  dr = get_distance_vector(pos_a, pos_b)
  print(dr.length)
  if dr:
    return dr
  else:
    return Vector2(0,0)