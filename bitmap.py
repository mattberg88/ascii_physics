from colors import *
from matth import *
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
screen_offset = Vector2(2, -10)
display_surface = pygame.display.set_mode(size)

cell_size = 5
bitmap = [[]]
bit_dims = bit_width, bit_height = int(width/cell_size), int(height/cell_size)

gravity = Vector2(0, 0.2)
decay_rate = 0.007
frame_rate = 30
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, pos, character, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, bounding_box=Vector2(1, 1),  name=''):
    self.pos = pos
    self.pos_pix = Vector2(pos.x * cell_size, pos.y * cell_size)
    self.character = character
    self.rgdbdy = rgdbdy
    self.collided = False
    self.inertia = inertia
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.bounding_box = bounding_box
    self.name = name
    self.step = 0

  def physics(self):
    stasis_step = Vector2(self.inertia.x * (1 - self.step), self.inertia.y * (1 - self.step))
    if self.step < 1:
      self.step = self.step + decay_rate
      self.inertia = stasis_step
    # constant gravity
    if not self.collided:
      self.inertia = self.inertia + gravity
    # apply inertia vector to pos
      self.pos = self.pos + Vector2(self.inertia.x, self.inertia.y)

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if bounds_collided(self, o):
          self.collided = True
          dvect = get_direction_vector(self.pos_pix, o.pos_pix)
          collision_point = Vector2(self.pos_pix.x + dvect.x, self.pos_pix.y + dvect.y)
          rebound_vector = get_direction_vector(collision_point, self.pos_pix).normalize()
          print('rebound vector: {}'.format(rebound_vector))
          pygame.draw.circle(screen, green, collision_point, 3)
          self.inertia = Vector2(self.inertia.x * rebound_vector.x * self.bounce_factor, self.inertia.y + rebound_vector.y * self.bounce_factor)
          self.step = 0
        else:
          self.collided = False

  def update(self):
    if self.rgdbdy:
      self.physics()
      self.detect_collisions()

    if self.pos.y >= bit_height-1: self.pos.y = bit_height-1
    if self.pos.y <= 1: self.pos.y = 1
    if self.pos.x >= bit_width-1: self.pos.x = bit_width-1
    if self.pos.x <= 1: self.pos.x = 1
    self.pos_pix = Vector2(self.pos.x * cell_size, self.pos.y * cell_size)


def refresh_bitmap(rows, columns):
  btmp = []
  for y in range(rows):
    bits = []
    for x in range(columns):
      bits.append(0)
      # bits.append(Bit(i * width + j, 0, Vector2(i * cell_size, j * cell_size)))
    btmp.append(bits)
  return np.array(btmp)

objs_in_scene = []

cursor_cube = Obj(Vector2(0,0), 2)
objs_in_scene.append(cursor_cube)

for i in range(50):
  floor_obj = Obj(Vector2(i + bit_width/4, 80), 6, False, bounding_box=Vector2(1,1))
  objs_in_scene.append(floor_obj)
# for j in range(10):
#   test_obj = Obj(Vector2(j * 2 + bit_width/3, 5), 2, True, Vector2(-1 + j/5,0), bounce_factor=1.1)
#   objs_in_scene.append(test_obj)
test_obj = Obj(Vector2(40, 5), 1, True)
objs_in_scene.append(test_obj)
test_obj2 = Obj(Vector2(60, 5), 1, True)
objs_in_scene.append(test_obj2)


def update_bitmap():
  bitmap = refresh_bitmap(bit_width, bit_height)
  for obj in objs_in_scene:
    obj.update()
    bitmap[int(obj.pos.y), int(obj.pos.x)] = obj.character
  return bitmap

def read_bitval(bitval):
  bit_index = ' oO0@*-.'
  return bit_index[bitval]

def render():
  mouse_pos = pygame.mouse.get_pos()
  cursor_cube.pos = Vector2((mouse_pos[0] - 7)/cell_size, (mouse_pos[1] + 1)/cell_size)
  bitmap = update_bitmap()

  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      text = font.render(str(read_bitval(entry)), True, white)
      display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    render()
    pygame.display.update()
    clock.tick(frame_rate)