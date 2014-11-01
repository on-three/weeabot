#!/usr/bin/env python
"""
capture_window_480.py

"""
import cygwinreg
import argparse

def set_registry(top, left, width, height):
  '''set screen capture recorder registry settings
  to desired pos and dimensions
  '''
  cap = cygwinreg.OpenKey(
    cygwinreg.HKEY_CURRENT_USER,
    "Software\\screen-capture-recorder", 0, cygwinreg.KEY_ALL_ACCESS
    )
  values = ['capture_height', 'capture_width', 'start_x', 'start_y',]
  #for value in values:  
  #  v, t = cygwinreg.QueryValueEx(cap, value)
  #  print "{v} is {value}".format(v=v, value=value)
  set_value(cap, 'start_x', left)
  set_value(cap, 'start_y', top)
  set_value(cap, 'capture_width', width)
  set_value(cap, 'capture_height', height)
  #never capture the mouse pointer.
  set_value(cap, 'capture_mouse_default_1', 0)
  
def set_value(key, subkey, value):
  #first echo the current value
  v, t = cygwinreg.QueryValueEx(key, subkey)
  print "{subkey} initial value {v} and type {t}".format(subkey=subkey, v=v, t=str(t))
  cygwinreg.SetValueEx(key, subkey, 0, t, value)

  v, t = cygwinreg.QueryValueEx(key, subkey)
  print "{subkey} final value {v}".format(subkey=subkey, v=v)
  
  
def main():
  #parser = argparse.ArgumentParser(description='Exercise bing translation api.')
  #parser.add_argument('text', help='Input text to translate.', type=str)
  #args = parser.parse_args()
  set_registry(100, 400, 848, 480)

if __name__ == "__main__":
  main()

