from utils import *
import sys, pygame, math
import numpy as np
from pygame import Vector2

pygame.init()

clock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen_offset = Vector2(-5, -10)
border_width = 5
cursor_border_width = 2
display_surface = pygame.display.set_mode(size)
cell_size = 10
max_inertia = 5
bit_width, bit_height = int(width/cell_size), int(height/cell_size)
bit_array = []
for y in range(bit_height):
  bits = []
  for x in range(bit_width):
    bits.append(0)
  bit_array.append(bits)
bitmap = np.array(bit_array)
gravity = Vector2(0, 0.5)
terminal_velocity = 3
decay_rate = 0.001
frame_rate = 30
font = pygame.font.SysFont('Arial', 18, bold=True)

bit_dict = {
  0: { 'character': '', 'offset': Vector2(0, 0)},
  1: { 'character': '.', 'offset': Vector2(0,0)},
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
}
char_dict = {
  0: { 'character': "(||')", 'offset': Vector2(0, 0)},
  1: { 'character': "( '')=", 'offset': Vector2(1,0)},
  2: { 'character': "( '')//", 'offset': Vector2(1, 0)},
  3: { 'character': "(` `)||", 'offset': Vector2(1, 0)},
  4: { 'character': "\\\('' )", 'offset': Vector2(-1, 0)},
  5: { 'character': "=('' )", 'offset': Vector2(-1, 0)}
}