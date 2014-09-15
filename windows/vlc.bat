#Begin batch file
cd c:\program files (x86)\VideoLAN\VLC
start /b vlc -vvv -I dummy dshow:// :dshow-aspect-ratio=16\:9 --sout=#transcode{vcodec=h264,vb=800,fps=25,scale=Auto,width=848,height=480,acodec=mpga,ab=128,channels=2,samplerate=44100}:http{mux=ts,dst=:8082/source} :sout-keep
