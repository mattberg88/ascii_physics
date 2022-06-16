import sys
import pygame
from src import *

#TODO: figure out why cant shoot straight
#TODO: improve bounce decay

btmp = Bitmap(bit_width, bit_height, border_width, 1)
cursor_obj = Obj(len(btmp.scene.sprites()) + 1, Vector2(0,0), 13, 'cursor', btmp.bitmap, True)
btmp.scene.add(cursor_obj)

def read_controls(keys, mouse):
  mouse_pos = mouse.get_pos()
  mouse_presses = mouse.get_pressed()
  if keys[pygame.K_a]:
    cursor_obj.real_pos += Vector2(-1, 0)
  if keys[pygame.K_d]:
    cursor_obj.real_pos += Vector2(1, 0)
  if keys[pygame.K_SPACE]:
      if btmp.bitmap[int(cursor_obj.pos.y + 1), int(cursor_obj.pos.x)] != 0:
        cursor_obj.energy = 1
        cursor_obj.inertia = cursor_obj.inertia + Vector2(0, -3)
  if mouse_presses[0]:
    if cursor_obj.shot: return
    bullet_pos = Vector2(int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
    bd_vector = get_distance_vector(bullet_pos, cursor_obj.real_pos+ cursor_obj.offset)
    bullet = Obj(2, cursor_obj.real_pos + cursor_obj.offset, 4, 'bullet', btmp.bitmap, True, inertia=-bd_vector, life_span=2)
    bullet.energy = 10
    btmp.scene.add(bullet)
    cursor_obj.shot = True

def render(bm):
  for y, row in enumerate(bm.bitmap):
    for x, entry in enumerate(row):
      if entry != 0 and entry <= len(btmp.scene.sprites()):
        cur_obj =  btmp.scene.sprites()[entry - 1]
        text = font.render(str(cur_obj.dict[cur_obj.char_index]['character']), True, white)
        display_surface.blit(text, (Vector2(x * cell_size + screen_offset.x, y * cell_size + screen_offset.y)))

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    if event.type == pygame.MOUSEBUTTONUP:
      cursor_obj.shot = False
  screen.fill(black)
  keys = pygame.key.get_pressed()
  mouse = pygame.mouse
  # mouse_pos = mouse.get_pos()
  # crosshairs_pos = Vector2(int(mouse_pos[0]/cell_size), int(mouse_pos[1]/cell_size))
  # crosshairs_obj.pos = crosshairs_pos
  # cursor_obj.char_index = animate_chara(bit_width, bit_height, crosshairs_pos)
  read_controls(keys, mouse)
  btmp.update()
  render(btmp)
  pygame.display.update()
  clock.tick(frame_rate)
