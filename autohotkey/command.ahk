
if 0 != 1
{
  ExitApp
}

IfWinExist SlingPlayer
{
  WinActivate
  SetKeyDelay, 500 
  Send %1%
}

Return