# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
'''

Module: screen.py
Desc: abstract installation configurations into one module
Author: on_three
Email: on.three.email@gmail.com
DATE: Friday, Dec 26th, 2014

Abstracted access to current stream screen size
  
'''

class Screen(object):
  '''
  screen size and other stream properties.
  '''
  WIDTH = 1280
  HEIGHT = 720
  TOP = 120
  LEFT = 600
  
  
def width():
  return Screen.WIDTH
  
def height():
  return Screen.HEIGHT
  
def top():
  return Screen.TOP
  
def left():
  return Screen.LEFT