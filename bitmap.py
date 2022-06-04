from colors import *
from matth import *
from bit_utils import *
import numpy as np
import sys, pygame, math
from pygame.math import Vector2
pygame.init()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
# invisible mouse when in window

clock = pygame.time.Clock()
size = width, height = 1000, 500
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
gravity = Vector2(0, 1)
terminal_velocity = 3
decay_rate = 0.2
frame_rate = 60
font = pygame.font.SysFont('Arial', 18, bold=True)

def generate_scene(config):
  scene = []
  idx = 1
  if config == 1:
    for i in range(20):
      floor_obj = Obj(idx, Vector2(bit_width/4 + i, bit_height - cell_size), 6, 'floor')
      scene.append(floor_obj)
      idx += 1
    test_obj = Obj(idx, Vector2(bit_width/2, border_width + cell_size), 1, 'test', True)
    scene.append(test_obj)
    idx += 1

  elif config == 2:
    for i in range(20):
      floor_obj = Obj(idx, Vector2(bit_width/4 + i, bit_height - cell_size), 6, 'floor')
      scene.append(floor_obj)
      idx += 1
    for j in range(20):
      for k in range(int(20)):
        test_obj = Obj(idx, Vector2(border_width + j, border_width + k), 5, 'test', True)
        scene.append(test_obj)
        idx += 1

  return scene

class Obj:
  def __init__(self, id, pos, char_index, name, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, mass=10):
    self.id = id
    self.pos = pos
    self.real_pos = pos
    self.mass = mass
    self.char_index = char_index
    self.character = bit_dict[char_index]['character']
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

  def physics(self):
    cm = bitmap_to_cm(bitmap, self.pos)
    bounce = collision_to_vec(cm)
    self.energy = max(0, self.energy - decay_rate)
    stasis_step = Vector2((self.inertia.x +  bounce.x) * self.energy, (self.inertia.y + bounce.y) * self.energy)
    if self.name != 'cursor':
      self.inertia = limit_vector(round_vector(stasis_step), 2)
      if bitmap[int(self.pos.y + 1), int(self.pos.x)] == 0 and self.inertia.length() < terminal_velocity:
        self.inertia = self.inertia + gravity
        # print(self.speed)
        self.energy = self.speed - decay_rate
      self.real_pos = self.real_pos + self.inertia
      self.real_pos = apply_border_threshold(bit_width, bit_height, border_width, self.real_pos)
    else:
      # print(cm)
      self.real_pos = apply_border_threshold(bit_width, bit_height, cursor_border_width, self.real_pos)
    bit_pos = int_vector(self.real_pos)
    map_pos_bit = bitmap[int(bit_pos.y), int(bit_pos.x)]
    if map_pos_bit != self.id and map_pos_bit != 0:
      self.real_pos += collision_to_move(cm)
    self.pos = int_vector(self.real_pos)
    # if self.name != 'cursor':
    #   print('inertia: {}, stasis_step : {}, energy: {}, speed: {}'.format(self.inertia, stasis_step , self.energy, self.speed))

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions and o not in self.collided and self.real_pos.distance_to(o.real_pos) < 1 :
        self.collided.append(o)
        self.inertia = self.inertia - o.speed_vector
        # self.energy = self.mass * self.speed**2
        self.energy = 1
      elif o in self.collided:
        self.collided.remove(o)

  def calculate_speed(self):
    self.speed_vector = get_distance_vector(self.real_pos, self.last_pos)
    dist = self.speed_vector.length()
    self.speed = round(dist * cell_size /40, 5)
    self.last_pos = self.real_pos

  def update(self):
    if self.rgdbdy:
      self.calculate_speed()
      self.detect_collisions()
      self.physics()
      # else:
      #   print(self.speed_vector, self.speed)

objs_in_scene = generate_scene(2)
cursor_obj = Obj(len(objs_in_scene) + 1, Vector2(0,0), 2, 'cursor', True)
objs_in_scene.append(cursor_obj)


def render_bitmap(bitmap):
  for y, row in enumerate(bitmap):
    for x, entry in enumerate(row):
      if entry != 0:
        char_index = objs_in_scene[entry - 1].char_index
        text = font.render(str(bit_dict[char_index]['character']), True, white)
        display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  screen.fill(black)
  mouse_pos = pygame.mouse.get_pos()
  cursor_offset = bit_dict[cursor_obj.char_index]['offset']
  cursor_obj.real_pos = Vector2(int((mouse_pos[0] + cursor_offset.x)/cell_size), int((mouse_pos[1] + cursor_offset.y)/cell_size))
  bitmap = update_bitmap(bit_width, bit_height, cursor_border_width, objs_in_scene)
  render_bitmap(bitmap)
  pygame.display.update()
  clock.tick(frame_rate)

