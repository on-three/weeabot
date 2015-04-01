'''
simple utilities

'''
import psutil
import win32con
import win32gui
import win32process
from twisted.python import log

def kill_proc_tree(pid, including_parent=True):    
  parent = psutil.Process(pid)
  for child in parent.children(recursive=True):
    child.kill()
  if including_parent:
    parent.kill()

def get_hwnds_for_pid (pid):
  print 'get_hwnds_for_pid ' + str(pid)
  def callback (hwnd, hwnds):
    _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
    if found_pid == pid:
      hwnds.append (hwnd)
    return True
  hwnds = []
  win32gui.EnumWindows(callback, hwnds)
  return hwnds
  
def activate_window_by_pid(pid):
  log.msg('activate_window_by_pid ' + str(pid))
  hwnds = get_hwnds_for_pid(pid);
  parent = psutil.Process(pid)
  for child in parent.children(recursive=True):
    get_hwnds_for_pid(child.pid)
    hwnds.extend(get_hwnds_for_pid(child.pid))
  for h in hwnds:
    try:
      win32gui.SetForegroundWindow(h)
    except:
      pass