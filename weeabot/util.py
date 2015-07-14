'''
simple utilities

'''
import psutil
import win32con
import win32gui
import win32process
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.internet import reactor

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
  
def activate_window_by_pid(pid, retries_remaining=10):
  log.msg('activate_window_by_pid ' + str(pid))
  hwnds = get_hwnds_for_pid(pid);
  parent = psutil.Process(pid)
  for child in parent.children(recursive=True):
    get_hwnds_for_pid(child.pid)
    hwnds.extend(get_hwnds_for_pid(child.pid))
  if not len(hwnds):
    log.msg("activate_window_by_pid: no hwnds found")
    #schedule another try in one second (max X retries)
    retries = retries_remaining - 1
    if retries:
      deferLater(reactor, 1, activate_window_by_pid, pid=pid, retries_remaining=retries)
    return False
  for h in hwnds:
    try:
      win32gui.SetForegroundWindow(h)
      #hack to always have our overlay atop any activated window.
      activate_window_by_name('weeabot_overlay')
    except:
      pass
      
def activate_window_by_name(name):
  log.msg('activate_window_by_name ' + name)
  window = win32gui.FindWindow(None, name)
  if window:
    win32gui.SetForegroundWindow(window)
  