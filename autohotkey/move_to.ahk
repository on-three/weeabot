
if 0 != 2
{
  MsgBox exiting
  ExitApp
}

IfWinExist SlingPlayer
{
  WinActivate
  CoordMode, Mouse, Relative
  MouseMove %1%, %2%
  ;Click %1%, %2%
}

Return