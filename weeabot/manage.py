#!/usr/bin/env python
# vim: set ts=2 expandtab:
import os
import sys

def main():
  '''
  Command line invocation
  '''
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weeabot.webserver.settings")
  from django.core.management import execute_from_command_line
  execute_from_command_line(sys.argv)

if __name__ == "__main__":
  '''
  It's standard practice to abstract the main() in python modules to aid loading
  '''
  main()

