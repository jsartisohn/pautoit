#!/usr/bin/python

import sys
import py2exe

from distutils.core import setup

sys.argv.append('py2exe')
setup(
  options = {
    'py2exe': {
      'includes': [
        'atk',
        'cairo',
        'gtk',
        'numpy',
        'pango',
        'pangocairo',
        'gio',
        'glib',
        'gobject',
        'numpy.core.multiarray',
        'win32api',
      ],
      'excludes': [
        'Tkinter',
        'win32ui',
        'win32pipe',
        'win32pdh',
        'unicodedata',
        'select',
        'numpy',
        'bz2',
        'pyexpat',
        'pyHook',  # We might potentially still need this for PyUserInput
      ],
      'ignores': ['gdk'],
      'dll_excludes': [
        'w9xpopen.exe',
        'CRYPT32.dll',
        'DNSAPI.DLL',
        'USP10.DLL',
        'MSIMG32.DLL',
      ],
      # We want bundle_files to be 1 to package everything we need into one
      # single .exe file. But py2exe appearently cannot package the freetype and
      # intl packages/.dlls into the .exe, so we're left to dump all required
      # into the dist directory.
      'bundle_files': 1,
      'optimize': 2,
      'compressed': True
    }
  },
  console=[{'script': 'pautoit.py'}],
  zipfile = None,
)
