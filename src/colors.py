import random

white = 225, 225, 225
grey = 150, 150, 150
black = 0, 0, 0
red = 255, 0, 0
yellow = 255, 255, 0
orange = 255, 150, 0
green = 0, 255, 0
purple = 255, 0, 255
blue = 0, 0, 255
cream = 255, 255, 200
cool_grey = 100, 130, 150
warm_grey = 150, 130, 100
def rainbow_color():
  r = random.randint(1 ,6)
  if r == 1:
    return red
  elif r == 2:
    return yellow
  elif r == 3:
    return orange
  elif r == 4:
    return green
  elif r == 5:
    return purple
  elif r == 6:
    return blue
