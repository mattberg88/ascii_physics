from pygame.math import Vector2

def generate_wall(top_pos, bottom_pos, cell_size, objs_in_scene, Obj):
  wall_height = (bottom_pos.y- top_pos.y)/cell_size
  for i in range(int(wall_height)):
    step = i * cell_size
    wall_obj = Obj('| |', Vector2(top_pos.x, top_pos.y + step), False, bounding_box=Vector2(cell_size, cell_size), name='wall_{}'.format(i))
    objs_in_scene.append(wall_obj)

def generate_floor(left_pos, right_pos, cell_size, objs_in_scene, Obj):
  floor_length = (right_pos.x - left_pos.x)/cell_size
  floor_obj1 = Obj('_' * int(floor_length), Vector2(left_pos.x, left_pos.y - 10), False, bounding_box=Vector2(0, 0), name='floor1')
  floor_obj2 = Obj('_' * int(floor_length), left_pos, False, bounding_box=Vector2(cell_size * floor_length, cell_size), name='floor2')
  objs_in_scene.append(floor_obj1)
  objs_in_scene.append(floor_obj2)
