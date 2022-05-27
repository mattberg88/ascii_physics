from matth import *
from colors import *
import sys, pygame, math
from pygame.math import Vector2
pygame.init()
clock = pygame.time.Clock()
seconds=(pygame.time.get_ticks())/1000
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
display_surface = pygame.display.set_mode(size)

gravity = Vector2(0, 1)
objs_in_scene = []
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, character, pos, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, bounding_box=Vector2(5, 5)):
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

  def prevent_fall(self):
    wall_r = width - 20
    wall_l = 20
    floor = height - 50
    if self.pos.y >= floor:
      self.collided = True
      self.pos = Vector2(self.pos.x, floor)
      self.inertia = self.inertia.reflect(Vector2(0, -1))
    else:
      self.collided = False
    if self.pos.x > wall_r:
      self.collided = True
      self.pos = Vector2(wall_r, self.pos.y)
      self.inertia = self.inertia.reflect(Vector2(-1, 0))
    else:
      self.collided = False
    if self.pos.x < wall_l:
      self.collided = True
      self.pos = Vector2(wall_l, self.pos.y)
      self.inertia = self.inertia.reflect(Vector2(1, 0))
    else:
      self.collided = False

  def detect_collision(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if bounds_collided(o, self):
          self.collided = True
          collision_rect = get_collision_rect(self, o)
          pygame.draw.rect(screen, green, collision_rect)
          cp = collision_rect.center
          rebound_dtv = get_direction_vector(Vector2(cp[0], cp[1]), self.pos)
          print('{} and {} dir: {}'.format(self.name, o.name, rebound_dtv))
          rebound_vector = rebound_dtv.normalize()
          self.inertia = self.inertia.reflect(rebound_vector)
          self.lerp = 0
        else:
          self.collided = False

  def update(self):
    if self.rgdbdy:
      self.physics()
      self.detect_collision()
    self.prevent_fall()

floor_obj = Obj('_'*100, Vector2(0, 400), False, bounding_box=Vector2(500, 5))

# for i in range(100):
#   floor_obj = Obj('_', Vector2(i * 5, 400), False, bounding_box=Vector2(10, 5))
objs_in_scene.append(floor_obj)

chars = 'oO0QD@#$%*'
for i, a in enumerate(chars):
  char_obj = Obj(a, Vector2(i * 50, i * 50), True, Vector2((i - 5), 0))
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