from colors import *
import random
import numpy as np
import sys, pygame
from pygame.math import Vector2
pygame.init()
clock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen_offset = Vector2(20, 15)
display_surface = pygame.display.set_mode(size)

cell_size = 30
bitmap = [[]]
bit_dims = bit_width, bit_height = int(width/cell_size), int(height/cell_size)

gravity = Vector2(0, 1)
decay_rate = 0.002
frame_rate = 24
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, pos, character, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, bounding_box=Vector2(cell_size, cell_size),  name=''):
    self.pos = pos
    self.character = character
    self.rgdbdy = rgdbdy
    self.inertia = inertia
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.bounding_box = bounding_box
    self.name = name
    self.step = 0

  def physics(self):
    self.pos = self.pos + gravity

  def update(self):
    print(self.pos)
    if self.rgdbdy and self.pos.y < 15:
      self.physics()

def initialize_np_bitmap(rows, columns):
  btmp = []
  for y in range(rows):
    bits = []
    for x in range(columns):
      bits.append(0)
      # bits.append(Bit(i * width + j, 0, Vector2(i * cell_size, j * cell_size)))
    btmp.append(bits)
  return np.array(btmp)

# CONFIGS:

# wall_l_obj = generate_wall(Vector2(10,100), Vector2(10, 400), cell_size, objs_in_scene, Obj)
# wall_r_obj = generate_wall(Vector2(width-20,100), Vector2(width-20, 400), cell_size, objs_in_scene, Obj)
# floor_obj = generate_floor(Vector2(0,400), Vector2(500, 400), cell_size, objs_in_scene, Obj)

# cursor_cube = Obj(100, 'O', Vector2(50, 50))
# objs_in_scene.append(cursor_cube)
# def update_bitmap():
#   for ob in objs_in_scene:
#     bitmap
# particle_count = 300
# for i in range(particle_count):
#   step_size = width/particle_count
#   step = (random.random() * step_size)
#   char_obj = Obj('o', Vector2(i * step_size + 20, 200), True, Vector2((random.random()-0.5) * 10, 0))
#   objs_in_scene.append(char_obj)

objs_in_scene = []

test_obj = Obj(Vector2(5, 1), 'O', True)
objs_in_scene.append(test_obj)
def update_bitmap():
  bitmap = initialize_np_bitmap(bit_width, bit_height)
  for obj in objs_in_scene:
    obj.update()
    bitmap[int(obj.pos.y), int(obj.pos.x)] = 1
  return bitmap

def render():
  mouse_pos = pygame.mouse.get_pos()
  # cursor_cube.pos = Vector2(mouse_pos[0] - 20, mouse_pos[1] - 10)
  bitmap = update_bitmap()
  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      text = font.render(str(entry), True, white)
      display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    render()
    pygame.display.update()
    clock.tick(frame_rate)