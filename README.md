#weeabot

Python Twisted based Japanese support irc bot.

Weeabot currently provides the following support via a simple plugin architecture:

* Japanese word lookup via Jisho.org.
* English to Japanese word lookup via Jisho.org.
* Display current Tokyo time in Japanese.
* Transliterate words and phrases into katakana via sci.lang.jp web tool.
* Control of a local slingbox player via autohotkey (windows only).
* Lookup of Japanese TV schedules fia the テレビ王国 site, including current and next program.
* Translaton of phrases via Bing Translate
* Auto translation of TV schedules scraped off テレビ王国.
* Automatic playing of posted .webm files (atop a video stream, for example).
* ~~IRC lookups inserted into SQL backend.~~
* ~~Django web interface for viewing and manipulating lookup history.~~
* ~~Formation of vocabulary lists via web interface.~~

Regarding the removed functionality above (sql and web backend) I'm currently maintainting them in the https://github.com/on-three/weeabot_site.git repository. I'm as yet unsure how this original bot and the updated bot/webserver will coexist.

##Using the Bot


Currently the bot supports the current commands:

### .h (help/list plugins)
Type bot should pick up the weeabot single command (no preceeding words) and display current plugins.
```
me: .h
weeabot: currently loaded plugins: Jisho Moon Jikan Katakanize | source: https://github.com/on-three/weeabot
```

### Jisho (Japanese Word Lookup)
Use the jisho command to look up Japanese words (in romaji, hiragana, katakana or kanji) via jisho.org.
Command available by using the jisho command or simply '.j'.
```
me: .j watashi
weeabot: 私 | わたし | watashi | I; me

```

### Moon (English to Japanese Word Lookup)
Use the moon command (after 'moonrunes') to look up Japanese equivalents of English words.
Also available via '.m'
```
me: .m me
weeabot:  私 | わたし | watashi | I; me

```

### Jikan (Current Tokyo Time)
Use the jikan command to display current Tokyo time.
Command also available via '.t'.
```
me: .t
weeabot: 現在の東京時間 2014年01月20日 19時21分40秒 月

```

### Katakanize (transliterate words and phrases to katakana)
Use the katakanize command to approximate any kind of word or phrase into katakana. This preserves the old "youkousoo" functionality which transliterated nicks into katakana, but which has been removed ;_;.
Command also available via '.k'.
It's clear the web serviced used here is very spotty, however.
```
me: katakanize on_three
weeabot:---> オン・スリー

```

### Channel (Slingbox Control)
This is perhaps the most complex, so i can only summarize here.
* `.c list` List channels available
* `.c up` or `.c down` Next channel up or down the dial
* `.c <channel name>` Change slingbox to that channel
* `.c air` `.c cable` or `.c bs` Change slingbox tuner
* `.c last` go to last channel (if known)

### Nani (tv schedule)
Scrape Terebi Oukoku for current channel info in Japanese.
```
.n animax 
weeabot [字]ガラスの仮面 #17 | 09/23 (火) 14:00 ~ 14:30 (30分) | 
http://tv.so-net.ne.jp/past/40067014003.action

.n animax next
weeabot: 魔法のプリンセス ミンキーモモ リマスター版 #17 | 09/23 (火) 14:30 ~ 15:00 (30分) | 
http://tv.so-net.ne.jp/past/40067014303.action

```

###Whatson (tv schedule english translation)
Fetch current tv schedule info and translate to English.
```
.w animax
weeabot: "[S] glass mask # 17" | 09/23 (火) 14:00 ~ 14:30 (30分) | 
http://tv.so-net.ne.jp/past/40067014003.action

.w animax next
weeabot: "Magical Princess minky Momo remastered edition # 17" | 09/23 (火) 14:30 ~ 15:00 (30分) | 
http://tv.so-net.ne.jp/past/40067014303.action

```

###Bing Translate
Simple Bing translate utility.
```
.b ガラスの仮面
weeabot: "Glass mask" 
```

###Stream info
Display current stream info if there is any
```
.i
| XXX | http:/XXX:XXX/XXX.ts | 480p 25fps (h264/mpga)ts |

.info
| XXX | http:/XXX:XXX/XXX.ts | 480p 25fps (h264/mpga)ts |

.streaminfo
| XXX | http:/XXX:XXX/XXX.ts | 480p 25fps (h264/mpga)ts |

```

###Webms
The webms plugin detects webms posted in a channel, and (currently) plays those webms in a local video player.
I have it configured localy so that these webms are played atop a desktop capture i'm streaming, superimposing the videos atop the stream.
The following commands can be used to simply control webm functionality:
* Turn webm playing on: ```.webms on```
* Turn webm playing off: ```.webms off```
* Stop all currently playing ```.wipe```

**Note** that only 4 webms can play at a time. Any above this limit (posted while 4 webs are already playing) will just be ignored.

##Lacking Functionality
The bot currently lacks the following:
* ~~the ability to have it sign into multiple channels.This could be added, but as yet I'm unsure how robust it would handle multiple~~ ~~simultaneous web lookups from multiple users in multiple channels. For the moment I'm content to run one bot per channel.~~
* I've also not done much work on testing the bot in how well it handles netsplits/kicks/bans. Don't know when i'll get to this.
* Lastly, even though I was sure to add support for IRC passwords (i.e. signing onto a znc server with password) I don't believe I've added support for irc registered nicks (i.e. NICKSERV). This could be added. Just haven't gotten to it yet.
* the SSL support is as yet _completely_ untested. I'd recommend just using non-ssl connections for the moment.


##Installation

I recommend installing via python pip package manager. Some python dependencies have tooling requirements, which can be handled on debian like systems by:
```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev

```
And it may be necessary to ensure that the japanese locale is available:
```
sudo apt-get install locales
sudo dpkg-reconfigure locales
```

The usual caveats of invoking a python virtual environment before installation apply. Use 'sudo' as required by your OS.
To install, point pip to:
```
sudo pip install git+https://github.com/on-three/weeabot.git
```
I've tested the above installation on LinuxMint 16 and Debian Squeeze, but no other distributions.

If you wish to install manually, invoke setup.py as usual:
```
sudo python setup.py install
```

The pip installation above should also install all required python dependencies. A list of these dependencies can be found in requirements.txt. Or you can install them manually using requirements.txt:
```
pip install -r requirements.txt
```

##Running

Installation via pip above (or running setup.py) should give you access to a 'weabot-daemon' command line executable. Help is available by simply typing the executable without arguments or with the -h switch:
```
(weeabot_irc)xxx@jxxxDesktop ~/code/weeabot $ weeabot-daemon
usage: weeabot-daemon [-h] [-u USERNAME] [-r REALNAME] [--password PASSWORD]
                      [--nickserv_pw NICKSERV_PW] [-v] [-s]
                      hostname nickname channel
weeabot-daemon: error: too few arguments

(weeabot_irc)xxx@xxxDesktop ~/code/weeabot $ weeabot-daemon -h
usage: weeabot-daemon [-h] [-u USERNAME] [-r REALNAME] [--password PASSWORD]
                      [--nickserv_pw NICKSERV_PW] [-v] [-s]
                      hostname nickname channel

Scrape jisho.org for japanese word (romaji) lookup.

positional arguments:
  hostname              IRC server URL as domain:port (e.g.
                        www.freenode.net:6660).
  nickname              Nick to use at signon. Multiple nicks not yet
                        supported.
  channel               Channel to join on server. Only supporting one channel
                        presently.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Username this server uses at IRC server signon.
  -r REALNAME, --realname REALNAME
                        Realname this server uses at IRC server signon.
  --password PASSWORD   Optional password this server uses at signon
  --nickserv_pw NICKSERV_PW
                        Optional password to use with nickserv after IRC
                        server connect.
  -v, --verbose         Run server in verbose mode.
  -s, --ssl             Connect to server via SSL.

```
Running from the command line is therefore usually just providing 1. hostname:port 2. bot nick 3. channels to join. N channels can be specified.
```
weeabot-daemon irc.network.net:6660 botname '#channel_one' '#channel_two' '#channel_three'
```

If the above weeabot-daemon comand line exe is not available on your system (for some reason) you could probably run it right from the weeabot.py script:
```
/path/to/weeabot/dir/weeabot.py irc.rizon.net:6660 botname '#channel'
```

##Logging

The bot currently logs its activity to a log at ~/.weeabot (i.e. hidden directory in user's home directory).
You can also see logging from the command line by using the -v switch (see command line options above).


##Daemon Support

If you don't want a command line window open all the time with weeabot running, I've put in some daemon support-- so the bot should start up automatically when your server starts. This is currently only for modern linux Debian systems with Upstart.
To do this, I've inlcuded two Upstart (new debian daemon management system) configuration scripts which can be used to  weeabot.conf and weeabot.override scripts to the /etc/init/ directory on Unix-like systems. This is meant as support for Upstart service management, allowing the bot to be run at system boot as a daemon.
In those systems that support Upstart .conf files, edit the /etc/init/weeabot.conf file to specify your IRC network, desired bot nick and channel to join. Other command line options can be added as needed. Then run the following to start the service:
```
sudo initclt reload-configuration
sudo start weeabot
```
From then on the bot can be started/stopped/restarted by simple commands:
```
sudo start weeabot
sudo restart weeabot
sudo stop weeabot
```

Delete or rename the /etc/init/weeabot.override file to enable automatic starting of daemon on boot.

