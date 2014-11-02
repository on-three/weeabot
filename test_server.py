#!/usr/bin/python

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def AddNicoNicoMsg(msg):
  print msg
  #print jsonrpclib.history.request
  return "success"

server = SimpleJSONRPCServer(('localhost', 9090))
server.register_function(pow)
server.register_function(lambda x,y: x+y, 'add')
server.register_function(lambda x: x, 'ping')
server.register_function(AddNicoNicoMsg)
server.serve_forever()