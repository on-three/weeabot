#!/usr/bin/python
# vim: set ts=2 expandtab:
"""

Module: weeabot.py
Desc: japanese dictionary IRC bot
Author: on_three
Email: on_three@outlook.com
DATE: Tuesday, Jan 14th 2013

Monitor IRC chat for posts starting with 'jisho'
and scrape following terms from jisho.org

Will implement simple japanese to english lookup and 
english to japanese lookup.
  
""" 

import os.path
import uuid
import sys
import time
from collections import defaultdict
import argparse
import string

from twisted.internet import task
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import ssl
from twisted.python import log
from twisted.words.protocols import irc as twisted_irc
import irc
import re

from twisted.web.client import getPage
from denshi_jisho import scrape_japanese_definitions

DEFAULT_PORT = 6660

JDICT_LOOKUP = 'jisho'
EDICT_LOOKUP = 'moon'
JISHO_USAGE = '\x033USAGE: jisho [japanese word to look up at jisho.org] [max results(default=3]'


class WeeaBot(twisted_irc.IRCClient):

  def connectionMade(self):
    print 'WeeaBot::connectionMade'
    twisted_irc.IRCClient.connectionMade(self)
    #self.factory.web_frontend.set_irc_socket(self)

  def connectionLost(self, reason):
    print 'WeeaBot::connectionLost'
    twisted_irc.IRCClient.connectionLost(self, reason)
    #self.factory.web_frontend.set_irc_socket(None)

  def signedOn(self):
    print 'WeeaBot::signedOn'
    '''
    Called when we've connected to the IRC server.
    We can use this opportunity to communicate with nickserv
    if necessary
    '''
    network = self.factory.network

    if network['identity']['nickserv_password']:
      self.msg('NickServ', 
            'IDENTIFY %s' % network['identity']['nickserv_password'])

    for channel in network['autojoin']:
      print('join channel %s' % channel)
      self.join(channel)

  def joined(self, channel):
    '''
    Called when we've joined a channel. This is here used to
    Initialize a chat dialog on the screen that will later
    be updated with posts as the chat progresses.
    '''
    print 'WeeaBot::joined'

    #joined_message = irc.JoinedMessage(channel)
    #self.factory.web_frontend.update_clients(joined_message)

  class JishoResponse(object):
    def __init__(self, callback_handler, channel):
      self._callback_handler = callback_handler
      self._channel = channel
      #self._num_defs = num_defs
    def __call__(self, response):
      self._callback_handler(response, self._channel)

  class JishoError(object):
    def __init__(self, callback_handler):
      self._callback_handler = callback_handler
    def __call__(self, response):
      self._callback_handler(response)

  def on_jisho_response(self, response, channel):
    results = scrape_japanese_definitions(response)
    if not results:
      self.say(channel, '\x034No results found at jisho.org using edict...')
      return
    for result in results:
      response = '\x035{result}'.format(result=result.encode('utf-8'))
      self.say(channel, response)

  def on_jisho_error(self, error):
    print error

  def handle_command(self, cmd, channel):
    args = string.split(cmd, ' ')
    jword = ''
    num_definitions = 3
    if len(args)<2:
      self.say(channel, JISHO_USAGE)
      return
    if len(args)>1:
      jword = args[1]
    if len(args)>2:
      try:
        num_definitions = int(args[2])
      except:
        pass
    print 'Looking up word {jword}'.format(jword=jword)
    result = getPage('http://jisho.org/words?jap={jword}&eng=&dict=edict'.format(jword=jword))
    result.addCallbacks(
      callback=WeeaBot.JishoResponse(self.on_jisho_response, channel),
      errback=WeeaBot.JishoError(self.on_jisho_error)
    )

  def privmsg(self, user, channel, msg):
    '''
    Invoked upon receipt of a message in channel X.
    '''
    msg = re.sub(' +',' ',msg)
    #1is this a command of interest?
    if msg.startswith(JDICT_LOOKUP):
      self.handle_command(msg, channel)

  def left(self, channel):
    pass
    #left_message = irc.LeftMessage(channel)
    #self.factory.web_frontend.update_clients(left_message)

  def noticed(self, user, channel, message):
    pass
    #notieced_msg = irc.NoticedMessage(user, channel, message)
    #self.factory.web_frontend.update_clients(notieced_msg)

  def modeChanged(self, user, channel, set, modes, args):
    pass
    #mode_changed_msg = irc.ModeChangedMessage(user, channel, set, modes, args)
    #self.factory.web_frontend.update_clients(mode_changed_msg)
    
  def kickedFrom(self, channel, kicker, message):
    pass
    #kicked_from_msg = irc.KickedFromMessage(channel, kicker, message)
    #self.factory.web_frontend.update_clients(kicked_from_msg)

  def NickChanged(self, nick):
    pass
    #nick_changed_msg = irc.NickChangedMessage(nick)
    #self.factory.web_frontend.update_clients(nick_changed_msg)

  def userJoined(self, user, channel):
    pass
    #user_joined_msg = irc.UserJoinedMessage(user, channel)
    #self.factory.web_frontend.update_clients(user_joined_msg)

  def userLeft(self, user, channel):
    pass
    #user_left_msg = irc.UserLeftMessage(user, channel)
    #self.factory.web_frontend.update_clients(user_left_msg)

  def userQuit(self, user, quit_message):
    pass
    #user_quit_msg = irc.UserQuitMessage(user, quit_message)
    #self.factory.web_frontend.update_clients(user_quit_msg)

  def userKicked(self, kickee, channel, kicker, message):
    pass
    #user_kicked_msg = irc.UserKickedMessage(kickee, channel, kicker, message)
    #self.factory.web_frontend.update_clients(user_kicked_msg)

  def action(self, user, channel, data):
    pass
    #action_msg = irc.ActionMessage(user, channel, data)
    #self.factory.web_frontend.update_clients(action_msg)

  def topicUpdated(self, user, channel, new_topic):
    pass
    #topic_updated_msg = irc.TopicUpdatedMessage(user, channel, new_topic)
    #self.factory.web_frontend.update_clients(topic_updated_msg)

  def userRenamed(self, oldname, newname):
    pass
    #user_renamed_msg = irc.UserRenamedMessage(oldname, newname)
    #self.factory.web_frontend.update_clients(user_renamed_msg)

  '''
  def irc_RPL_TOPIC(self, prefix, params):
    """
    Called when the topic for a channel is initially reported or when it      subsequently changes.
    params[0] is your nick
    params[1] is channel joined
    params[2] is topic for channel

    """
    print 'WeeaBot::irc_RPL_TOPIC'
    channel = params[1]
    topic = params[2]
    #topic = irc.formatting_to_pango_markup(topic)

    topic_message = irc.TopicMessage(channel, topic)
    self.factory.web_frontend.update_clients(topic_message)
'''
  def alterCollidedNick(self, nickname):
    print 'WeeaBot::alterCollidedNick'
    return nickname+'_'

class WeeaBotFactory(protocol.ClientFactory):
  protocol = WeeaBot

  def __init__(self, network_name, network):
    self.network_name = network_name
    self.network = network

  def clientConnectionLost(self, connector, reason):
    connector.connect()

  def clientConnectionFailed(self, connector, reason):
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
  parser.add_argument('nickname', help='Nick to use at signon. Multiple nicks not yet supported.', type=str)
  parser.add_argument('channel', help='Channel to join on server. Only supporting one channel presently.', type=str)
  #parser.add_argument('-p','--server_port', help='Port this server will service html client requests on. NOT the IRC server port this server connects to.', type=int, default=8888)
  parser.add_argument('-u', '--username', help='Username this server uses at IRC server signon.', type=str, default='')
  parser.add_argument('-r', '--realname', help='Realname this server uses at IRC server signon.', type=str, default='')
  parser.add_argument('--password', help='Optional password this server uses at signon', type=str, default=None)
  parser.add_argument('--nickserv_pw', help='Optional password to use with nickserv after IRC server connect.', type=str, default=None)
  parser.add_argument('-v', '--verbose', help='Run server in verbose mode.', action="store_true")
  parser.add_argument('-s', '--ssl', help='Connect to server via SSL.', action="store_true")
  args = parser.parse_args()

  hostname, port = split_server_port(args.hostname)
  if args.verbose:
    print 'Connecting to ' + hostname + ' on port ' + str(port) +'.'
    
  credentials = {
    'nickname': args.nickname,
    'realname': args.realname if len(args.realname)>0 else args.nickname,
    'username': args.username if len(args.username)>0 else args.nickname,
    'password': args.password,
    'nickserv_password': args.nickserv_pw
  }
  #we've got to add thise to the client, which is odd as fuq
  WeeaBot.nickname = credentials['nickname']
  WeeaBot.realname = credentials['realname']
  WeeaBot.username = credentials['username']
  WeeaBot.password = credentials['password']
    
  channels = (args.channel,)

  network = {
    'host': hostname,
    'port': port,
    'ssl': args.ssl,
    'identity': credentials,
    'autojoin': channels
  }


  factory = WeeaBotFactory(hostname, network)
  if args.ssl:
    reactor.connectSSL(hostname, port, factory, ssl.ClientContextFactory())
  else:
    reactor.connectTCP(hostname, port, factory)

  reactor.run()


if __name__ == "__main__":
  log.startLogging(sys.stdout)
  main()
