#!/usr/bin/python

import sys
import time

from pykeyboard import PyKeyboard
from pymouse import PyMouse
from region import Region

mouse = PyMouse()
keyboard = PyKeyboard()

screen_width, screen_height = mouse.screen_size()
r = Region(0, 0, screen_width, screen_height)

print '''This is a demo that takes control of you mouse and keyboard.
 So don't freak out and don't interfere if you don't want random things to
 happen to your Master Race PC.
 Press enter when you're ready.'''
raw_input()

# Demo imports
import random
import string
random.seed(1337)
for i in range(10):
  print '=' * 80
  # Screen pixel colors
  pos = (random.randint(0, screen_width), random.randint(0, screen_height))
  print 'Color at position %s is %s' % (pos, r.color_at(*pos))
  # Screen pixel colors 2
  x, y = (random.randint(0, screen_width), random.randint(0, screen_height))
  print 'Red   at position %s is %s' % ((x, y), r.color_at(x, y)[0])
  print 'Green at position %s is %s' % ((x, y), r.color_at(x, y)[1])
  print 'Blue  at position %s is %s' % ((x, y), r.color_at(x, y)[2])
  # Mouse movement
  pos = (random.randint(0, screen_width), random.randint(0, screen_height))
  print 'Setting mouse position to (%s - %s)' % pos
  mouse.move(*pos)
  # Keyboard input
  key = random.choice(string.lowercase)
  print 'Pressing %s button on the keyboard.' % key
  keyboard.tap_key(key)
  sys.stdout.flush()
  time.sleep(0.2)

# As reference, methods I didn't want to use in the demo:
#
# keyboard.press_key(k.alt_key)
# keyboard.tap_key(k.tab_key)
# keyboard.release_key(k.alt_key)
# mouse.click(1337, 42)
