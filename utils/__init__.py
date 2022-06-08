import numpy as np
import sys, pygame, math
import random
from pygame.math import Vector2
from pygame.sprite import Sprite
from utils.colors import *
from utils.constants import *
from utils.bit_utils import *
from bitmap import *

# pygame.init()
# pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
class Obj(Sprite):
  def __init__(self, id, pos, char_index, name, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=5, mass=10, dict=bit_dict, life_span=None, stopper=False):
    self.id = id
    self.pos = pos
    self.real_pos = pos
    self.mass = mass
    self.char_index = char_index
    self.character = dict[char_index]['character']
    self.offset = dict[char_index]['offset']
    self.rgdbdy = rgdbdy
    self.inertia = inertia
    self.speed_vector = Vector2(0,0)
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.energy = 1
    self.last_pos = self.pos
    self.collided = []
    self.speed = 0
    self.last_tick = pygame.time.get_ticks()
    self.name = name
    self.life_span = life_span
    self.dict = dict
    self.shot = False
    self.stopper = stopper
    Sprite.__init__(self)

  def physics(self):
    cm = bitmap_to_cm(bitmap, self.pos)
    bounce = collision_to_vec(cm)
    if self.name == 'cursor': bounce = Vector2(0,0)
    if self.name != 'bullet':
      self.inertia = self.inertia + gravity
      self.energy = max(0, self.energy - decay_rate)
    stasis_step = Vector2((self.inertia.x +  bounce.x) * self.energy, (self.inertia.y + bounce.y) * self.energy)
    self.inertia = limit_vector(round_vector(stasis_step, 2), 2)
    self.real_pos = self.real_pos + self.inertia
    self.real_pos = apply_border_threshold(bit_width, bit_height, border_width, self.real_pos)
    bit_pos = int_vector(self.real_pos)
    map_pos_bit = bitmap[int(bit_pos.y), int(bit_pos.x)]
    if map_pos_bit != self.id and map_pos_bit != 0:
      self.real_pos += collision_to_move(cm)
    self.pos = int_vector(self.real_pos)
    # if self.name == 'cursor':
    #   print('inertia: {}, stasis_step : {}, energy: {}, speed: {}'.format(self.inertia, stasis_step , self.energy, self.speed))

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions and o not in self.collided:
        if self.real_pos.distance_to(o.real_pos) < 1 and self.name != 'cursor':
          if not self.stopper:
            self.collided.append(o)
            self.inertia = self.inertia - (o.speed_vector * self.bounce_factor)
            # self.energy = self.mass * self.speed**2
            self.energy = 1
          else:
            if o.name == 'bullet':
              self.stopper = False
              self.energy = 1
      elif o in self.collided:
        self.collided.remove(o)


  def calculate_speed(self):
    self.speed_vector = get_distance_vector(self.real_pos, self.last_pos)
    if self.name != 'cursor': self.char_index = speed_to_char(self.speed_vector)
    dist = self.speed_vector.length()
    self.speed = round(dist * 10 /40, 5)
    self.last_pos = self.real_pos

  def update(self):
    if self.life_span:
      if self.life_span <= 0:
        objs_in_scene.remove(self)
        self.kill()
        return
      self.life_span = self.life_span - 0.1
    if self.rgdbdy:
      self.calculate_speed()
      if self.collisions:
        self.detect_collisions()
      if not self.stopper:
        self.physics()

# invisible mouse when in window
def generate_scene(config):
  scene = []
  idx = 1
  if config == 1:
    for i in range(bit_width):
      floor_obj = Obj(idx, Vector2(i, bit_height - border_width), 3, 'floor')
      scene.append(floor_obj)
      idx += 1
    test_obj = Obj(idx, Vector2(bit_width/2, border_width + cell_size), 1, 'test', True)
    scene.append(test_obj)
    idx += 1

  elif config == 2:
    for i in range(bit_width):
      floor_obj = Obj(idx, Vector2(i, bit_height - border_width), 3, 'floor')
      scene.append(floor_obj)
      idx += 1
    for j in range(10):
      for k in range(int(10)):
        test_obj = Obj(idx, Vector2(bit_width - border_width - j, bit_height - 2 * (border_width) - k), 5, 'test', True, stopper=False)
        scene.append(test_obj)
        idx += 1

  return scene

#scene setup

# crosshairs_obj = Obj(len(objs_in_scene) + 1, Vector2(0,0), 4, 'crosshairs', collisions=False)
# objs_in_scene.append(crosshairs_obj)

def render_bitmap(bitmap):
  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      if entry != 0 and entry <= len(objs_in_scene):
        cur_obj =  objs_in_scene[entry - 1]
        text = font.render(str(cur_obj.dict[cur_obj.char_index]['character']), True, white)
        display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

def read_controls(keys, mouse):
  mouse_pos = mouse.get_pos()
  mouse_presses = mouse.get_pressed()
  if keys[pygame.K_a]:
    cursor_obj.real_pos += Vector2(-1, 0)
  if keys[pygame.K_d]:
    cursor_obj.real_pos += Vector2(1, 0)
  if keys[pygame.K_SPACE]:
      if bitmap[int(cursor_obj.pos.y + 1), int(cursor_obj.pos.x)] != 0:
        cursor_obj.energy = 1
        cursor_obj.inertia = cursor_obj.inertia + Vector2(0, -3)
  if mouse_presses[0]:
    if cursor_obj.shot: return
    bullet_pos = Vector2(int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
    bd_vector = get_distance_vector(bullet_pos, cursor_obj.real_pos+ cursor_obj.offset)
    bullet = Obj(2, cursor_obj.real_pos + cursor_obj.offset, 4, 'bullet', True, inertia=-bd_vector, life_span=2)
    bullet.energy = 10
    objs_in_scene.append(bullet)
    cursor_obj.shot = True


def generate_scene(config):
  scene = []
  idx = 1
  if config == 1:
    for i in range(bit_width):
      floor_obj = Obj(idx, Vector2(i, bit_height - border_width), 3, 'floor', dict=bit_dict)
      scene.append(floor_obj)
      idx += 1
    test_obj = Obj(idx, Vector2(bit_width/2, border_width + cell_size), 1, 'test', True, dict=bit_dict)
    scene.append(test_obj)
    idx += 1

  elif config == 2:
    for i in range(bit_width):
      floor_obj = Obj(idx, Vector2(i, bit_height - border_width), 3, 'floor', dict=bit_dict)
      scene.append(floor_obj)
      idx += 1
    for j in range(10):
      for k in range(int(10)):
        test_obj = Obj(idx, Vector2(bit_width - border_width - j, bit_height - 2 * (border_width) - k), 5, 'test', True, stopper=False, dict=bit_dict)
        scene.append(test_obj)
        idx += 1

  return scene

objs_in_scene = generate_scene(1)
cursor_obj = Obj(len(objs_in_scene) + 1, Vector2(0,0), 0, 'cursor', True, dict=char_dict)
objs_in_scene.append(cursor_obj)

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.MOUSEBUTTONUP:
      cursor_obj.shot = False
  screen.fill(black)
  keys = pygame.key.get_pressed()
  mouse = pygame.mouse
  mouse_pos = mouse.get_pos()
  crosshairs_pos = Vector2(int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
  # crosshairs_obj.pos = crosshairs_pos
  cursor_obj.char_index = animate_chara(bit_width, bit_height, crosshairs_pos)
  read_controls(keys, mouse)
  bitmap = update_bitmap(bit_width, bit_height, cursor_border_width, objs_in_scene)
  render_bitmap(bitmap)
  pygame.display.update()
  clock.tick(frame_rate)