import random
import numpy as np
import pygame
from src.colors import *
from pygame import Vector2

pygame.init()
# pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

clock = pygame.time.Clock()
size = width, height = 400, 300
screen = pygame.display.set_mode(size)
screen_offset = Vector2(-5, -10)
border_width = 5
display_surface = pygame.display.set_mode(size)
cell_size = 10
max_inertia = 5
bit_width, bit_height = int(width/cell_size), int(height/cell_size)
gravity = Vector2(0, 0.5)
terminal_velocity = 3
decay_rate = 0.05
frame_rate = 24
font = pygame.font.SysFont('Arial', 18, bold=True)

bit_dict = {
  0: { 'character': '', 'offset': Vector2(0, 0)},
  1: { 'character': '.', 'offset': Vector2(0, 0)},
  2: { 'character': ',', 'offset': Vector2(0, 0)},
  3: { 'character': '-', 'offset': Vector2(0, 0)},
  4: { 'character': '+', 'offset': Vector2(0, 0)},
  5: { 'character': '*', 'offset': Vector2(0, 0)},
  6: { 'character': 'o', 'offset': Vector2(0, 0)},
  7: { 'character': 'O', 'offset': Vector2(0, 0)},
  8: { 'character': '|', 'offset': Vector2(0, 0)},
  9: { 'character': '~', 'offset': Vector2(0, 0)},
  10: { 'character': '-', 'offset': Vector2(0, 0)},
  11: { 'character': '/', 'offset': Vector2(0, 0)},
  12: { 'character': "\\", 'offset': Vector2(0, 0)},
  13: { 'character': "ï", 'offset': Vector2(0, 0)},
}

