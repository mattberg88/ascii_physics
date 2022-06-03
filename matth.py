import pygame
import math
from pygame.math import Vector2

def vector_mult(pos_a, pos_b):
  return Vector2(pos_a.x * pos_b.x, pos_a.y * pos_b.y)

def get_distance_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)
