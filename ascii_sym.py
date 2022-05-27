from matth import *
from colors import *
import random
import sys, pygame
from pygame.math import Vector2
pygame.init()
clock = pygame.time.Clock()
seconds=(pygame.time.get_ticks())/1000
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
display_surface = pygame.display.set_mode(size)

gravity = Vector2(0, 1)
#collision box size per unit
char_size = 5
objs_in_scene = []
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, character, pos, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, bounding_box=Vector2(char_size, char_size)):
    self.character = character
    self.pos = pos
    self.rgdbdy = rgdbdy
    self.inertia = inertia
    self.collisions = collisions
    self.collided = False
    self.bounce_factor = bounce_factor
    self.bounding_box = bounding_box
    self.name = character[0]
    self.lerp = 0

  def physics(self):
    # step inertia towards homeostasis
    stasis_step = Vector2(self.inertia.x * (1 - self.lerp), self.inertia.y * (1 - self.lerp))
    if self.lerp < 1:
      self.lerp = self.lerp + 0.005
      self.inertia = stasis_step
    if not self.collided:
      self.inertia = self.inertia + gravity
      self.pos = self.pos + self.inertia

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if bounds_collided(o, self):
          self.collided = True
          collision_rect = get_collision_rect(self, o)
          # pygame.draw.rect(screen, green, collision_rect)
          collision_point = Vector2(collision_rect.center[0], collision_rect.center[1])
          rebound_dv = get_direction_vector(collision_point, self.pos)
          rebound_vector = rebound_dv.normalize()
          print('{} and {} rebound_dv: {} rebound_vector: {}'.format(self.name, o.name, rebound_dv, rebound_vector))
          self.pos = self.pos + rebound_dv
          self.inertia = Vector2(self.inertia.x * round(rebound_vector.x), self.inertia.y * round(rebound_vector.y))
          self.lerp = 0
        else:
          self.collided = False

  def update(self):
    if self.rgdbdy:
      self.physics()
      self.detect_collisions()

# def generate_wall(top_pos, bottom_pos):
#   wall_height = (top_pos.y - bottom_pos.y)/char_size
#   return Obj('|\n' * int(wall_height), top_pos, False, bounding_box=Vector2(char_size, char_size * wall_height))

def generate_floor(left_pos, right_pos):
  floor_length = (right_pos.x - left_pos.x)/char_size
  return Obj('_' * int(floor_length), left_pos, False, bounding_box=Vector2(char_size * floor_length, char_size))



floor_obj = generate_floor(Vector2(0,400), Vector2(500, 400))
objs_in_scene.append(floor_obj)

chars = 'oO0QD@#$%'
for i, a in enumerate('oO0QD@#$%'):
  step_size = width/len(chars)
  char_obj = Obj(a, Vector2(i * step_size, 100), True, Vector2( random.randint( -5, 5), 0))
  objs_in_scene.append(char_obj)

def render():
  for object in objs_in_scene:
    text = font.render(str(object.character), True, white)
    display_surface.blit(text, (object.pos))
    object.update()

while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()
    screen.fill(black)
    render()
    pygame.display.update()
    clock.tick(60)