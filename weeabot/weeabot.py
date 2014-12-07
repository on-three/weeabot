#! /usr/bin/env python
# vim: set ts=2 expandtab:
"""

Module: weeabot.py
Desc: japanese dictionary IRC bot
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, Jan 14th 2013

 Simple Japanese support IRC bot for weeaboos.
 Primitive plugin architecture provides stuff like:
 * Japanese word lookup
 * English to Japanese word lookup
 * Current Tokyo time
  
""" 

import os
import os.path
from os.path import expanduser
import re
import uuid
import sys
import time
import argparse
import string

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import ssl
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.words.protocols import irc as twisted_irc

from config import Config


#for now directly import plugins
from jisho import Jisho
from jikan import Jikan
from moon import Moon
#from youkoso import Youkoso
from katakanize import Katakanize
from slingbox import Slingbox
from bangumi import Bangumi
from translate import Translate
from whatson import Whatson
from info import Info
from webms import Webms
from config import Config
#from textoverlay import TextOverlay

DEFAULT_PORT = 6660
LOG_FILENAME = '{botname}.weeabot.log'.format(botname=Config.BOTNAME)
LOG_DIRECTORY = '/.weeabot'

#Don't use global data! lel
RETURN_CODE = 0

#after http://stackoverflow.com/questions/938870/python-irc-bot-and-encoding-issue
def irc_decode(bytes):
  '''
  IRC character encoding can be arbitrary. python doesn't like this
  '''
  try:
    text = bytes.decode('utf-8')
  except UnicodeDecodeError:
    try:
      text = bytes.decode('iso-8859-1')
    except UnicodeDecodeError:
      text = bytes.decode('cp1252')
  return text


def irc_encode(bytes):
  '''
  IRC character encoding can be arbitrary. python doesn't like this
  '''
  try:
    text = bytes.encode('utf-8')
  except UnicodeEncodeError:
    try:
      text = bytes.encode('iso-8859-1')
    except UnicodeEncodeError:
      text = bytes.encode('cp1252')
  return text


class WeeaBot(twisted_irc.IRCClient):
  plugins = []
  COMMAND_REGEX = r'^(?P<command>\.h(elp)?( )?)'

  def connectionMade(self):
    log.msg('connection made')
    twisted_irc.IRCClient.connectionMade(self)
    WeeaBot.plugins.append(Jisho(self))
    WeeaBot.plugins.append(Moon(self))
    WeeaBot.plugins.append(Jikan(self))
    WeeaBot.plugins.append(Katakanize(self))
    #self.youkoso = Youkoso(self)
    WeeaBot.plugins.append(Slingbox(self))
    WeeaBot.plugins.append(Bangumi(self))
    WeeaBot.plugins.append(Translate(self))
    WeeaBot.plugins.append(Whatson(self))
    WeeaBot.plugins.append(Info(self))
    WeeaBot.plugins.append(Webms(self))
    #WeeaBot.plugins.append(TextOverlay(self))

  def connectionLost(self, reason):
    log.msg('connection lost')
    RETURN_CODE = -1
    twisted_irc.IRCClient.connectionLost(self, reason)

  def signedOn(self):
    '''
    Called when we've connected to the IRC server.
    We can use this opportunity to communicate with nickserv
    if necessary
    '''
    log.msg('signed on')
    network = self.factory.network

    if network['identity']['nickserv_password']:
      self.msg('NickServ', 
            'IDENTIFY %s' % network['identity']['nickserv_password'])

    #NO LONGER AUTOJOIN MULTIPLE CHANNELS
    #Just join the one from the config
    self.join(Config.CHANNEL.encode('utf-8'))
    #for channel in network['autojoin']:
    #  log.msg('join channel %s' % channel)
    #  self.join(channel)

  def joined(self, channel):
    '''
    Called when we've joined a channel. This is here used to
    Initialize a chat dialog on the screen that will later
    be updated with posts as the chat progresses.
    '''
    log.msg(u'{botname}::joined'.format(botname=Config.BOTNAME).encode('utf-8'))

  def privmsg(self, user, channel, msg):
    '''
    Invoked upon receipt of a message in channel X.
    Give plugins a chance to handle it until one does
    '''
    #issue #5. UTF-8 decoding fails sometimes in plugins
    #so we'll try to decode into unicode here. If it fails we ignore.
    try:
      msg = msg.decode('utf-8')
    except UnicodeDecodeError:
      log.msg('privmsg ' + msg)
      return
    #log.msg(u'privmsg ' + msg)
    self.handle_msg(user, channel, msg)

  def handle_msg(self, user, channel, msg):
    '''
    Generic handler for all msgs in channel.
    '''
    #msg = re.sub(' +',' ',msg)
    if re.match(WeeaBot.COMMAND_REGEX, msg):
      plugins = self.list_loaded_plugins()
      help = plugins + u'| source: https://github.com/on-three/weeabot'
      self.say(channel, help.encode('utf-8'))
      return
      
    for plugin in WeeaBot.plugins:
      if plugin.is_msg_of_interest(user, channel, msg):
        #we check interest over all channels, but only pass messages to the channel we're on
        #this allows us to have some plugins process messages via private message, but others ignore them.
        if channel != Config.CHANNEL:
          continue
        plugin.handle_msg(user, channel, msg)
        break

  def left(self, channel):
    pass

  def noticed(self, user, channel, message):
    log.msg('noticed ' + message)

  def modeChanged(self, user, channel, set, modes, args):
    pass
    
  def kickedFrom(self, channel, kicker, message):
    if channel == Config.CHANNEL:
      RETURN_CODE = -1
      reactor.stop()

  def NickChanged(self, nick):
    pass

  def userJoined(self, user, channel):
    '''
    Special handling if user joins channel
    '''
    #self.youkoso.initiate_welcome(user, channel)
    pass

  def userLeft(self, user, channel):
    #self.youkoso.initiate_farewell(user, channel)
    pass

  def userQuit(self, user, quit_message):
    #self.youkoso.initiate_farewell(user, channel=user)
    pass

  def userKicked(self, kickee, channel, kicker, message):
    #self.youkoso.initiate_farewell(kickee, channel=kickee)
    pass

  def action(self, user, channel, data):
    pass

  def topicUpdated(self, user, channel, new_topic):
    pass

  def userRenamed(self, oldname, newname):
    pass

  '''
  def who(self, channel):
    self.sendLine('WHO %s' % channel)

  def irc_RPL_WHOREPLY(self, *nargs):
    print 'WHO:', nargs

  def irc_RPL_ENDOFWHO(self, *nargs):
    print 'WHO COMPLETE'
  '''
  def alterCollidedNick(self, nickname):
    return nickname+'_'

  def list_loaded_plugins(self):
    '''
    Return a string with a list of all the currently loaded plugins
    '''
    plugins = u'currently loaded plugins: '
    for plugin in WeeaBot.plugins:
      plugins += u'{plugin} '.format(plugin=plugin.__class__.__name__)
    return plugins

class WeeaBotFactory(protocol.ClientFactory):
  protocol = WeeaBot

  def __init__(self, network_name, network):
    self.network_name = network_name
    self.network = network

  def clientConnectionLost(self, connector, reason):
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
    RETURN_CODE = -1
    reactor.stop()


def split_server_port(hostname):
  port = DEFAULT_PORT
  if not ':' in hostname:
    return (hostname, DEFAULT_PORT)
  hostname, port = string.split(hostname, ':', maxsplit=1)
  try:
    port = int(port)
  except ValueError:
    port = DEFAULT_PORT
  return (hostname, port)


def main():
  parser = argparse.ArgumentParser(description='Scrape jisho.org for japanese word (romaji) lookup.')
  parser.add_argument('hostname', help='IRC server URL as domain:port (e.g. www.freenode.net:6660).', type=str)
  #parser.add_argument('nickname', help='Nick to use at signon. Multiple nicks not yet supported.', type=str)
  #parser.add_argument('channels', nargs='*', help='Channel(s) to join on server.', type=str)
  #parser.add_argument('-p','--server_port', help='Port this server will service html client requests on. NOT the IRC server port this server connects to.', type=int, default=8888)
  parser.add_argument('-u', '--username', help='Username this server uses at IRC server signon.', type=str, default='')
  parser.add_argument('-r', '--realname', help='Realname this server uses at IRC server signon.', type=str, default='')
  parser.add_argument('--password', help='Optional password this server uses at signon', type=str, default=None)
  parser.add_argument('--nickserv_pw', help='Optional password to use with nickserv after IRC server connect.', type=str, default=None)
  parser.add_argument('-v', '--verbose', help='Run server in verbose mode.', action="store_true")
  parser.add_argument('-s', '--ssl', help='Connect to server via SSL.', action="store_true")
  args = parser.parse_args()


  #always log to daily file in ~/.weeabot unlesss we have verbose option
  if args.verbose:
    log.startLogging(sys.stdout)
  else:
    HOME = expanduser("~")
    log_directory = HOME+LOG_DIRECTORY
    if not os.path.exists(log_directory):
      os.makedirs(log_directory)
    log_file = DailyLogFile(LOG_FILENAME, log_directory)
    log.startLogging(log_file)
    

  hostname, port = split_server_port(args.hostname)
  if args.verbose:
    print 'Connecting to ' + hostname + ' on port ' + str(port) +'.'

  nick = Config.BOTNAME.encode('utf-8')
  credentials = {
    'nickname': nick,
    'realname': args.realname if len(args.realname)>0 else nick,
    'username': args.username if len(args.username)>0 else nick,
    'password': args.password,
    'nickserv_password': args.nickserv_pw
  }
  #we've got to add thise to the client, which is odd as fuq
  WeeaBot.nickname = credentials['nickname']
  WeeaBot.realname = credentials['realname']
  WeeaBot.username = credentials['username']
  WeeaBot.password = credentials['password']
    
  #channels = args.channels
  #print str(channels)

  network = {
    'host': hostname,
    'port': port,
    'ssl': args.ssl,
    'identity': credentials,
    #'autojoin': channels
  }

  factory = WeeaBotFactory(hostname, network)
  if args.ssl:
    reactor.connectSSL(hostname, port, factory, ssl.ClientContextFactory())
  else:
    reactor.connectTCP(hostname, port, factory)

  reactor.run()
  sys.exit(RETURN_CODE)

if __name__ == "__main__":
  main()
