
if 0 != 2
{
  MsgBox exiting
  ExitApp
}

IfWinExist SlingPlayer
{
  WinActivate
  Send !o
  WinWait, Options, , 3
  IfWinExist Options
  {
    WinActivate
    CoordMode, Mouse, Relative
    MouseMove 75, 44
    Click 75, 44
    ;select the menu item
    MouseMove 400,115
    Click 400,115
    Click %1%, %2%
    ;Click 400,135 ;automatic
    ;Click 400,190 ;720
    ;Click 400,200 ;480
  }
  IfWinExist Options
  {
    CoordMode, Mouse, Relative
    Click 190, 561 ;ok
  }
}


Return