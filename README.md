weeabot
=======

Python Twisted based Japanese support irc bot.

Weeabot currently provides the following support via a simple plugin architecture:

* Japanese word lookup via Jisho.org.
* English to Japanese word lookup via Jisho.org.
* Display current Tokyo time in Japanese.
* Transliterate words and phrases into katakana via sci.lang.jp web tool.
* IRC lookups inserted into SQL backend.
* Django web interface for viewing and manipulating lookup history.
* Formation of vocabulary lists via web interface.

Installation
------------

I recommend installing via python pip package manager. The usual caveats of invoking a python virtual environment before installation apply. Use 'sudo' as required by your OS.
To install, point pip to:
```
sudo pip install git+https://github.com/on-three/weeabot.git
```
I've tested the above installation on LinuxMint 16 and Debian Squeeze, but no other distributions.

If you wish to install manually, invoke setup.py as usual:
```
sudo python setup.py install
```

Daemon Support
--------------

Proper installation should install weeabot.conf and weeabot.override scripts to the /etc/init/ directory on Unix-like systems. This is meant as support for Upstart service management, allowing the bot to be run at system boot as a daemon.

In those systems that support Upstart .conf files, edit the /etc/init/weeabot.conf file before starting, specifying your IRC network, desired bot nick and channel to join. Other command line options can be added as needed. Then run the following to start the service:
```
sudo initclt reload-configuration
sudo start weeabot
```

Delete or rename the /etc/init/weeabot.override file to enable automatic starting of daemon on boot.

Using the Bot
-------------

Currently the bot supports the current commands:

### weeabot (list plugins)
Type bot should pick up the weeabot single command (no preceeding words) and display current plugins.
```
me: weeabot
weeabot: currently loaded plugins: Jisho Moon Jikan
```

### Jisho (Japanese Word Lookup)
Use the jisho command to look up Japanese words (in romaji, hiragana, katakana or kanji) via jisho.org.
Command available by using the jisho command or simply '.j'.
```
me: jisho watashi
weeabot: 私 | わたし | watashi | I; me

me: .j わたし
weeabot: 私 | わたし | watashi | I; me

me: .j 私
weeabot: 私 | わたし | watashi | I; me
```

### Moon (English to Japanese Word Lookup)
Use the moon command (after 'moonrunes') to look up Japanese equivalents of English words.
Also available via '.m'
```
me: moon me
weeabot:  私 | わたし | watashi | I; me

me: .m me
weeabot:  私 | わたし | watashi | I; me
```

### Jikan (Current Tokyo Time)
Use the jikan command to display current Tokyo time.
Command also available via '.t'.
```
me: jikan
weeabot: 現在の東京時間 2014年01月20日 19時21分40秒 月

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

me: .k on_three
weeabot:---> オン・スリー
```
