#from pykeyboard import PyKeyboard
import time
import sys

from Xlib import display
data = display.Display().screen().root.query_pointer()._data





import gtk.gdk

def pixel_at(x, y):
  rw = gtk.gdk.get_default_root_window()
  pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
  pixbuf = pixbuf.get_from_drawable(rw, rw.get_colormap(), x, y, 0, 0, 1, 1)
  return tuple(pixbuf.pixel_array[0, 0])

from pymouse import PyMouse
m = PyMouse()

import numpy
light_gray = numpy.array([42, 42, 42], dtype=numpy.uint8)
light_red = numpy.array([213,  83,  54], dtype=numpy.uint8)
dark_red = numpy.array([194, 75, 49], dtype=numpy.uint8)
light_blue = numpy.array([53, 184, 213], dtype=numpy.uint8)
dark_blue = numpy.array([48, 167, 194], dtype=numpy.uint8)

gray = "gray"
red = "red "
blue = "blue"
border = "wall"

num_x = 10
num_y = num_x
step_x = 60
step_y = step_x
width = num_x * step_x
height = num_y * step_y
start_x = 2250
start_y = 275

def get_10x10_colors():
  rw = gtk.gdk.get_default_root_window()
  pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, width, height)
  pixbuf = pixbuf.get_from_drawable(
    rw, rw.get_colormap(), start_x, start_y, 0, 0, width, height)
  result = [[None for y in range(num_y)] for x in range(num_y)]
  for y in range(num_y):
    for x in range(num_x):
      color = pixbuf.pixel_array[y * step_y, x * step_x]
      if(color == light_gray).all():
        result[y][x] = gray
      elif (color == light_blue).all() or (color == dark_blue).all():
        result[y][x] = blue
      elif (color == light_red).all() or (color == dark_red).all():
        result[y][x] = red
      else:
        return False
  return result


def done(field):
  if not field:
    print "Invalid field."
    return True
  for y in field:
    for x in y:
      if x == gray:
        return False;
  return True

def opposite(c):
  if c == red:
    return blue
  elif c == blue:
    return red
  else:
    print "No opposite for %s" % c
    sys.exit(1)

class Step:
  def __init__(self, x, y, c):
    self.x = x
    self.y = y
    self.c = c

def get_next_step(field):
  finished_rows = []
  prefinished_rows = []
  finished_cols = []
  prefinished_cols = []
  col_blues = [0] * num_y
  col_reds = [0] * num_y
  for y in range(num_y):
    row_blues = 0
    row_reds = 0
    for x in range(num_x):
      c = field[y][x]
      if c == red:
        col_reds[x] +=1
        row_reds +=1
      elif c == blue:
        col_blues[x] +=1
        row_blues +=1;
      if x-1 >= 0:
        c_left = field[y][x-1]
      else:
        c_left = border
      if x+1 < num_x:
        c_right = field[y][x+1]
      else:
        c_right = border
      if y-1 >= 0:
        c_top = field[y-1][x]
      else:
        c_top = border
      if y+1 < num_y:
        c_bottom = field[y+1][x]
      else:
        c_bottom = border
      #print "     %s     " % (c_top)
      #print "%s %s %s" % (c_left, c, c_right)
      #print "     %s     " % (c_bottom)
      #print "========="
      # Adjacency checks
      if c != gray:
        if c == c_left and c_right == gray:
          return Step(x+1, y, opposite(c))
        elif c == c_right and c_left == gray:
          return Step(x-1, y, opposite(c))
        elif c == c_top and c_bottom == gray:
          return Step(x, y+1, opposite(c))
        elif c == c_bottom and c_top == gray:
          return Step(x, y-1, opposite(c))
        else:
          pass
      else:
        if c_left != gray and c_left == c_right :
          return Step(x, y, opposite(c_left))
        elif c_top != gray and c_top == c_bottom:
          return Step(x, y, opposite(c_top))
        else:
          pass
      # Line sum checks
      rowcolor = gray
      if row_blues == num_x / 2:
        rowcolor = red
      elif row_reds == num_x / 2:
        rowcolor = blue
      else:
        pass
      if rowcolor != gray:
        for x_2 in range(num_x):
          if field[y][x_2] == gray:
            return Step(x_2, y, rowcolor)
    # cache some stuff for same line comparison at the end
    if row_reds + row_blues == num_x:
      finished_rows += [y]
    elif row_reds + row_blues == num_x - 2:
      prefinished_rows += [y]
    else:
      pass
  # Column sum checks
  for x_2 in range(num_y):
    colcolor = gray
    if col_reds[x_2] == num_y / 2:
      colcolor = blue
      colcolornum = x_2
    elif col_blues[x_2] == num_y / 2:
      colcolor = red
      colcolornum = x_2
    else:
      pass
    if colcolor != gray:
      for y_2 in range(num_y):
        if field[y_2][x_2] == gray:
          return Step(x_2, y_2, colcolor)
    # Coumn same line comparison stuff
    if col_reds[x_2] + col_blues[x_2] == num_y:
      finished_cols += [x_2]
    elif col_reds[x_2] + col_blues[x_2] == num_y - 2:
      prefinished_cols += [x_2]
  for prow in prefinished_rows:
    for frow in finished_rows:
      fail = False
      g = None
      for x in range(num_x):
        if field[prow][x] == gray:
          g = x
        elif field[prow][x] == field[frow][x]:
          pass
        else:
          fail = True
          break
      if not fail:
        return Step(g, prow, opposite(field[frow][g]))
  for pcol in prefinished_cols:
    for fcol in finished_cols:
      fail = False
      g = None
      for y in range(num_y):
        if field[y][pcol] == gray:
          g = y
        elif field[y][pcol] == field[y][fcol]:
          pass
        else:
          fail = True
          break
      if not fail:
        return Step(pcol, g, opposite(field[g][fcol]))

  # Oh noes! We need to compare nearly finished lines with finished ones to
  # avoid duplicating them. Efficient algorithms are hard. Let's do it greedy!


  print "End of current logic :("
  sys.exit(1)



field = get_10x10_colors()
i = 0
while not done(field):
  i += 1
  next_step = get_next_step(field)
  print "Next step: %s - %s : %s " % (next_step.x, next_step.y, next_step.c)
  sys.stdout.flush()
  x = start_x + next_step.x * step_x
  y = start_y + next_step.y * step_y
  #raw_input()
  m.click(x, y)
  time.sleep(0.2)
  if next_step.c == blue:
    m.click(x, y)
    time.sleep(0.2)
  field = False
  while not field:
    field = get_10x10_colors()
