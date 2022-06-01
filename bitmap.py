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
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
screen_offset = Vector2(-5, -10)
border_width = 2
display_surface = pygame.display.set_mode(size)

cell_size = 10
max_inertia = 5
bit_width, bit_height = int(width/cell_size), int(height/cell_size)

gravity = Vector2(0, 0.1)
decay_rate = 0.05
frame_rate = 24
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, pos, char_index, name, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1):
    self.pos = pos
    self.char_index = char_index
    self.character = bit_dict[char_index]['character']
    self.rgdbdy = rgdbdy
    self.inertia = inertia
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.energy = 0
    self.collided = []
    self.last_pos = self.pos
    self.speed = Vector2(0,0)
    self.name = name

  def physics(self):
    stasis_step = Vector2(self.inertia.x * self.energy, self.inertia.y * self.energy)
    if self.energy > 0:
      self.energy = self.energy - decay_rate
      self.inertia = stasis_step
    self.inertia = self.inertia + gravity
    self.pos = self.pos + self.inertia


  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if self.pos.distance_to(o.pos) < 1 and o not in self.collided:
          self.collided.append(o)
          d = get_direction_vector(self.pos, o.pos)
          d_norms = d.normalize()
          if o.rgdbdy:
            self.inertia = Vector2(((self.inertia.x * -d_norms.x) + o.inertia.x) * self.bounce_factor, ((self.inertia.y * -d_norms.y) + o.inertia)  * self.bounce_factor)
            self.energy = 1
          else:
            # self.pos = self.pos - self.inertia
            i = self.inertia - d
            self.pos = self.pos - self.inertia
            self.inertia = Vector2(i.x * self.bounce_factor, i.y * self.bounce_factor)
            print('self: {} self pos: {} other pos: {} dr: {} inertia: {}'.format(self.character, self.pos, o.pos, -d_norms, self.inertia))
        if self.pos.distance_to(o.pos) >= 1 and o in self.collided:
          self.collided.remove(o)


  def calculate_speed(self):
    if self.last_pos != self.pos:
      self.speed = get_direction_vector(self.pos, self.last_pos)
      self.last_pos = self.pos

  def update(self):
    if self.rgdbdy or self.name == 'cursor':
      self.calculate_speed()
      self.physics()
      self.detect_collisions()
      self.pos = apply_border_threshold(bit_width, bit_height, border_width, self.pos)
    self.last_pos = self.pos

objs_in_scene = []

cursor_obj = Obj(Vector2(0,0), 2, False, 'cursor')
objs_in_scene.append(cursor_obj)

for i in range(bit_width - 1):
  floor_obj = Obj(Vector2(border_width/2 + i, bit_height - cell_size), 6, 'floor')
  objs_in_scene.append(floor_obj)
# for j in range(20):
#   for k in range(int(20)):
#     test_obj = Obj(Vector2(bit_width/2 + j, border_width + k), 7, True)
#     objs_in_scene.append(test_obj)
test_obj = Obj(Vector2(bit_width/2, border_width), 1, 'test', True)
objs_in_scene.append(test_obj)

def render_bitmap(bitmap):
  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      text = font.render(str(bit_dict[entry]['character']), True, white)
      display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

  # fps = str(int(clock.get_fps()))
  # if fps != last_fps:
  #   print('fps: {}'.format(clip(clock.get_fps())))
  #   last_fps = fps
while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  screen.fill(black)
  mouse_pos = pygame.mouse.get_pos()
  cursor_offset = bit_dict[cursor_obj.char_index]['offset']
  cursor_obj.pos = Vector2((mouse_pos[0] + cursor_offset.x)/cell_size, (mouse_pos[1] + cursor_offset.y)/cell_size)
  bitmap = blank_bitmap(bit_width, bit_height)
  bitmap = update_bitmap(bitmap, 1, objs_in_scene)
  render_bitmap(bitmap)
  pygame.display.update()
  clock.tick(frame_rate)

