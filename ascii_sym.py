from matth import *
from colors import *
from generators import *
import random
import sys, pygame
from pygame.math import Vector2
pygame.init()
clock = pygame.time.Clock()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
display_surface = pygame.display.set_mode(size)

# CONFIGS:
gravity = Vector2(0, 0.5)
decay_rate = 0.002
cell_size = 5
frame_rate = 24


objs_in_scene = []
font = pygame.font.SysFont('Arial', 18, bold=True)

class Obj:
  def __init__(self, character, pos, rgdbdy=False, inertia=Vector2(0,0), collisions=True, bounce_factor=1, bounding_box=Vector2(cell_size, cell_size), draw_bb=False, name=''):
    self.character = character
    self.pos = pos
    self.rgdbdy = rgdbdy
    self.inertia = inertia
    self.collisions = collisions
    self.bounce_factor = bounce_factor
    self.bounding_box = bounding_box
    self.collided = False
    self.draw_bb = draw_bb
    self.name = name
    self.step = 0

  def physics(self):
    # step inertia towards homeostasis
    stasis_step = Vector2(self.inertia.x * (1 - self.step), self.inertia.y * (1 - self.step))
    if self.step < 1:
      self.step = self.step + decay_rate
      self.inertia = stasis_step
    # constant gravity
    if not self.collided:
      self.inertia = self.inertia + gravity
      # apply inertia vector to pos
      self.pos = self.pos + self.inertia

  def detect_collisions(self):
    for o in objs_in_scene:
      if o != self and o.collisions:
        if bounds_collided(o, self):
          self.collided = True
          collision_rect = get_collision_rect(self, o)
          # pygame.draw.rect(screen, green, collision_rect)
          collision_point = Vector2(collision_rect.center[0], collision_rect.center[1])
          rebound_vector = get_direction_vector(collision_point, self.pos).normalize()
          self.pos = self.pos + rebound_vector
          self.inertia = Vector2(self.inertia.x * rebound_vector.x * self.bounce_factor, self.inertia.y * rebound_vector.y * self.bounce_factor)
          self.step = 0
        else:
          self.collided = False


  def update(self):
    if self.rgdbdy:
      self.physics()
      self.detect_collisions()

wall_l_obj = generate_wall(Vector2(10,100), Vector2(10, 400), cell_size, objs_in_scene, Obj)
wall_r_obj = generate_wall(Vector2(width-20,100), Vector2(width-20, 400), cell_size, objs_in_scene, Obj)
floor_obj = generate_floor(Vector2(0,400), Vector2(500, 400), cell_size, objs_in_scene, Obj)

cursor_cube = Obj('(o_o)', Vector2(0,0), False, bounding_box=Vector2(20, 20), name='cursor')
objs_in_scene.append(cursor_cube)

particle_count = 100
for i in range(particle_count):
  step_size = width/particle_count
  step = (random.random() * step_size)
  char_obj = Obj('o', Vector2(i * step_size + 20, 200), True, Vector2((random.random()-0.5) * 10, 0))
  objs_in_scene.append(char_obj)

def render():
  mouse_pos = pygame.mouse.get_pos()
  cursor_cube.pos = Vector2(mouse_pos[0] - 20, mouse_pos[1] - 10)
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
    clock.tick(frame_rate)