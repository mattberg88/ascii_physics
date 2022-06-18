import sys
import pygame
from src import *

#TODO: figure out why cant shoot straight
#TODO: improve bounce decay

scene = Scene(bit_width, bit_height, border_width, 2)
cursor_obj = Obj(scene.idx, Vector2(4,4), 13, 'cursor', scene.bitmap, True, color=green)
scene.add_to_group(cursor_obj)

def read_controls(keys, mouse):
  mouse_pos = mouse.get_pos()
  mouse_presses = mouse.get_pressed()
  if keys[pygame.K_a]:
    cursor_obj.real_pos += Vector2(-1, 0)
  if keys[pygame.K_d]:
    cursor_obj.real_pos += Vector2(1, 0)
  if keys[pygame.K_SPACE]:
    cursor_obj.energy = 1
    if scene.bitmap[int(cursor_obj.pos.y + 1), int(cursor_obj.pos.x)] != 0:
      cursor_obj.inertia = cursor_obj.inertia + Vector2(0, -3)
    cursor_obj.inertia = cursor_obj.inertia + Vector2(0, -1)
  if mouse_presses[0]:
    if random.randint(0,1) == 0: return
    bullet_pos = Vector2(int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
    bd_vector = get_distance_vector(bullet_pos, cursor_obj.real_pos+ cursor_obj.offset)
    bullet = Obj(-1, cursor_obj.real_pos + cursor_obj.offset, 5, 'bullet', scene.bitmap, True, inertia=-bd_vector, life_span=5, color=red)
    bullet.energy = 10
    scene.add_bullet(bullet)

def render(scn):
  sprites = scene.group.sprites()
  for y, row in enumerate(scn.bitmap):
    for x, entry in enumerate(row):
      if entry != 0 and entry <= len(sprites):
        cur_obj = scene.get_by_id(entry)
        cur_obj.bitmap = scn.bitmap
        text = font.render(str(cur_obj.dict[cur_obj.char_index]['character']), True, cur_obj.color)
        display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  screen.fill(black)
  keys = pygame.key.get_pressed()
  mouse = pygame.mouse
  read_controls(keys, mouse)
  render(scene)
  pygame.display.update()
  clock.tick(frame_rate)
  scene.update()

