from src.constants import *
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.sprite import Group, Sprite

class Scene:
  def __init__(self, width, height, border, scene_config):
    self.bitmap = self.new_bitmap()
    self.width = width
    self.height = height
    self.border = border
    self.group = Group()
    self.scene_config = scene_config
    self.idx = 1

    if self.scene_config == 1:
      for i in range(self.width):
        floor_obj = Obj(self.idx, Vector2(i, self.height - self.border), 3, 'floor', self.bitmap, color=cool_grey)
        self.add_to_group(floor_obj)

      test_obj = Obj(self.idx, Vector2(self.width/2, self.border + cell_size), 1, 'test', self.bitmap , True, color=warm_grey)
      self.add_to_group(test_obj)

    elif self.scene_config == 2:
      for i in range(self.width - 3):
        floor_obj = Obj(self.idx, Vector2(i + 2, self.height - self.border), 3, 'floor',  self.bitmap, color=cool_grey)
        self.add_to_group(floor_obj)

      for j in range(10):
        for k in range(int(20)):
          test_obj = Obj(self.idx, Vector2(self.width - self.border - j, self.height - self.border - k -1), 5, 'test', self.bitmap , True, stopper=True, life_span=10, color=warm_grey)
          self.add_to_group(test_obj)

  def __getitem__(self, pos):
    return self.bitmap[pos[1], pos[0]]

  def get_by_id(self, id):
    return next((i for i in self.group if i.id == id), None)

  def new_bitmap(self):
    bit_array = []
    for y in range(height):
      bits = []
      for x in range(width):
        bits.append(0)
      bit_array.append(bits)
    return np.array(bit_array)

  def add_to_group(self, obj):
    self.group.add(obj)
    self.idx += 1
    print(self.idx)

  def remove_from_group(self, obj):
    self.group.remove(obj)

  def add_bullet(self, bullet):
    self.group.add(bullet)


  def update(self):
    bm = self.new_bitmap()
    self.group.update()
    for obj in self.group.sprites():
      if not obj.life_span or obj.life_span > 0:
        bm[int(obj.pos.y), int(obj.pos.x)] = obj.id
    self.bitmap = bm

class Obj(Sprite):
  def __init__(self, id, pos, char_index, name, btmp, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=5, mass=10, dict=bit_dict, life_span=None, stopper=False, color=white):
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
    self.stopper = stopper
    self.bitmap = btmp
    self.color = color
    Sprite.__init__(self)

  def physics(self):
    cm = bitmap_to_cm(self.bitmap, self.pos)
    bounce = collision_to_vec(cm)
    if self.name == 'cursor':
      bounce = Vector2(0,0)
      self.energy = 1
    if self.name != 'bullet':
      self.inertia = self.inertia + gravity
      self.energy = max(0, round(self.energy - decay_rate, 2))
    stasis_step = Vector2((self.inertia.x +  bounce.x) * self.energy, (self.inertia.y + bounce.y) * self.energy)
    stasis_rounded = Vector2(round(stasis_step.x, 2), round(stasis_step.y, 2))
    self.inertia = limit_vector(stasis_rounded, 2)
    self.real_pos = self.real_pos + self.inertia
    self.real_pos = apply_ground(bit_height-border_width -1, self.real_pos)
    bit_pos =  Vector2(int(self.real_pos.x), int(self.real_pos.y))
    map_pos_bit = self.bitmap[int(bit_pos.y), int(bit_pos.x)]
    map_under_bit = self.bitmap[int(bit_pos.y + 1), int(bit_pos.x)]
    if map_pos_bit != self.id and map_pos_bit != 0 and self.name != 'cursor':
      if map_under_bit == 0: self.energy = 1
      self.real_pos += collision_to_move(cm)
    self.pos = Vector2(int(self.real_pos.x), int(self.real_pos.y))
    # if self.name == 'test':
    #   print('inertia: {}, stasis_step : {}, energy: {}, speed: {}'.format(self.inertia, stasis_step , self.energy, self.speed))

  def detect_collisions(self):
    sprites = self.groups()[0].sprites()
    for o in sprites:
      if o != self and o.collisions and o not in self.collided:
        if self.real_pos.distance_to(o.real_pos) < 1 and self.name != 'cursor':
          if not self.stopper:
            self.collided.append(o)
            self.inertia = self.inertia - (o.speed_vector * self.bounce_factor)
            # self.energy = self.mass * self.speed**2
            self.energy = 1
          else:
            if o.name == 'bullet':
              Sound("sounds/brick.mp3").play()

              self.stopper = False
              self.energy = 1
      elif o in self.collided:
        self.collided.remove(o)

  def calculate_speed(self):
    self.speed_vector = get_distance_vector(self.real_pos, self.last_pos)
    if self.name != 'cursor' and self.name != 'bullet': self.char_index = speed_to_char(self.speed_vector)
    dist = self.speed_vector.length()
    self.speed = round(dist * 10 /40, 5)
    self.last_pos = self.real_pos

  def update(self):
    if self.life_span and not self.stopper:
      if self.life_span <= 0:
        self.inertia = Vector2(0,2)
        if self.name == 'bullet':
          return Sprite.kill(self)
      else: self.life_span = self.life_span - 0.1
    if self.rgdbdy:
      self.calculate_speed()
      if self.collisions:
        self.detect_collisions()
      if not self.stopper:
        self.physics()

def speed_to_char(speed_vector):
  x,y = speed_vector.x, speed_vector.y
  if (x > 0.5 and y > 0.5) or (x < -0.5 and y < -0.5): return 12
  if (x < -0.5 and y > 0.5) or (x > 0.5 and y < -0.5 ): return 11
  if abs(x) > 0.5 : return 3
  if abs(y) > 0.5 : return 8
  else: return 1

def get_distance_vector(pos_a, pos_b):
  return Vector2(pos_b.x - pos_a.x, pos_b.y - pos_a.y)

def apply_ground(limit, pos):
  p = Vector2(pos.x, pos.y)
  if p.y > limit:
    p.y = limit
  return p

def is_oob(width, height, border_width, pos):
  p = Vector2(pos.x, pos.y)
  if p.y > height:
    return True
  if p.x >= width-border_width:
    return True
  if p.x <= border_width:
    return True
  return False

def animate_chara(width, height, pos):
  x, y = pos[0], pos[1]
  if x == width/2 and y == height: return 0
  if x>width/2 and y>height - height/5: return 1
  if x<width/2 and y>height - height/5: return 5
  if x>width/2 and y>height/3: return 2
  if x<width/2 and y>height/3: return 4
  if x == width/2 and y<height/2: return 3
  return 0

def limit_vector(vec, limit):
  v = vec
  if v.x > limit:
    v.x = limit
  if v.x < -limit:
    v.x = -limit
  if v.y > limit:
    v.y = limit
  if v.y < -limit:
    v.y = -limit
  return v

def round_vector(vec, factor=5):
  return Vector2(round(vec.x, factor), round(vec.y, factor))

def bitmap_to_cm(bm, pos):
  center = bm[int(pos.y), int(pos.x)]
  top = bm[int(pos.y - 1), int(pos.x)]
  bottom = bm[int(pos.y + 1), int(pos.x)]
  left = bm[int(pos.y), int(pos.x - 1)]
  right = bm[int(pos.y), int(pos.x + 1)]
  l_top = bm[int(pos.y - 1), int(pos.x - 1)]
  r_top = bm[int(pos.y - 1), int(pos.x + 1)]
  l_bottom = bm[int(pos.y + 1), int(pos.x - 1)]
  r_bottom = bm[int(pos.y + 1), int(pos.x + 1)]
  return np.array([[l_top,top,r_top], [left,center,right], [l_bottom,bottom,r_bottom]])

def collision_to_vec(cm):
  d = Vector2(0, 0)
  for i, y in enumerate(cm):
    for j, x in enumerate(y):
      if x != 0:
        d = Vector2(d.x - (j-1), d.y - (i-1))
  if d.length() > 0:
    return d.normalize()
  else:
    return Vector2(0, 0)

def collision_to_move(cm):
  r_factor = random.randint(0,1)
  if r_factor == 0:
    if cm[1,0] == 0:
      return Vector2(-1, 0)
    elif cm[1,2] == 0:
      return Vector2(1, 0)
  else:
    if cm[1,2] == 0:
      return Vector2(1, 0)
    elif cm[1,0] == 0:
      return Vector2(-1, 0)
  if cm[0, 1] == 0:
    return Vector2(0, -1)
  elif cm[2, 1] == 0:
    return Vector2(0, 1)
  else:
    return Vector2(0, 0)
