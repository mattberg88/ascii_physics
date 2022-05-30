from colors import *
from matth import *
from bit_utils import *
import random
import numpy as np
import sys, pygame, math
from pygame.math import Vector2
pygame.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
# invisible mouse when in window

clock = pygame.time.Clock()
last_fps = 0
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
screen_offset = Vector2(-5, -10)
mouse_offset = Vector2(-8, 1)
border_width = 4
display_surface = pygame.display.set_mode(size)

cell_size = 5
max_inertia = 1
bit_dims = bit_width, bit_height = int(width/cell_size), int(height/cell_size)

gravity = Vector2(0, 0.2)
decay_rate = 0.05
frame_rate = 24
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, pos, char_index, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1,  name=''):
    self.pos = pos
    self.char_index = char_index
    self.character = bit_dict[char_index]['character']
    self.rgdbdy = rgdbdy
    self.collided = False
    self.inertia = inertia
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.bounding_box = bit_dict[char_index]['bounding_box']
    self.name = name
    self.step = 0

  def physics(self):
    stasis_step = Vector2(clip(self.inertia.x) * (1 - self.step), clip(self.inertia.y) * (1 - self.step))
    if self.step < 1:
      self.step = self.step + decay_rate
      self.inertia = stasis_step
      self.inertia = self.inertia + gravity

    # constant gravity
      self.inertia = self.inertia + gravity
  # apply inertia vector to pos
    self.pos = self.pos + Vector2(min(max_inertia, self.inertia.x), min(max_inertia, self.inertia.y))

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if bounds_collided(self, o):
          self.collided = True
          rebound_vector = get_direction_vector(o.pos, self.pos)
          collision_point = get_midway_point(o.pos, self.pos)

          rebound_vector = get_normal(collision_point, self.pos)
          # apply inertia in opposing direction
          self.inertia = Vector2(self.inertia.x + rebound_vector.x * self.bounce_factor, self.inertia.y + rebound_vector.y * self.bounce_factor)
          # print('self: {} self pos: {} other pos: {} rebound: {} inertia: {}'.format(self.character, self.pos, o.pos, rebound_vector, self.inertia))

          self.step = 0
        else:
          self.collided = False

  def update(self):
    if self.rgdbdy:
      self.pos = Vector2(clip(self.pos.x), clip(self.pos.y))
      self.physics()
      self.detect_collisions()
      self.pos = apply_border_threshold(bit_width, bit_height, border_width, self.pos)

objs_in_scene = []

cursor_cube = Obj(Vector2(0,0), 2)
objs_in_scene.append(cursor_cube)

for i in range(bit_width - 2):
  floor_obj = Obj(Vector2(border_width/2 + i, bit_height - cell_size), 6, False)
  objs_in_scene.append(floor_obj)
for j in range(5):
  for k in range(int(bit_width/3)):
    test_obj = Obj(Vector2(bit_width/3 + k, border_width + j), 7, True)
    objs_in_scene.append(test_obj)

def render_bitmap(bitmap):
  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      text = font.render(str(bit_dict[entry]['character']), True, white)
      display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

def render():
  mouse_pos = pygame.mouse.get_pos()
  cursor_cube.pos = Vector2((mouse_pos[0] + mouse_offset.x)/cell_size, (mouse_pos[1] + mouse_offset.y)/cell_size)
  bitmap = update_bitmap(bit_width, bit_height, 1, objs_in_scene)
  render_bitmap(bitmap)
  fps = str(int(clock.get_fps()))
  if fps != last_fps:
    print('fps: {}'.format(clip(clock.get_fps())))
    last_fps = fps

while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    render()
    pygame.display.update()
    clock.tick(frame_rate)