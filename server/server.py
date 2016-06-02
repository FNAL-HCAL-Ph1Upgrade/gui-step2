#!/usr/bin/python
#
#server.py
#command server to run on RPi and receive commands to send via i2c

#use python 3's print instead of python 2's print
from __future__ import print_function

#Server imports
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

#For parsing, logging
import time
import re

#For i2c
from smbus import SMBus

#setup
VERBOSITY = 2
bus = SMBus(1)
t = time.localtime()
logfilename = '%s_%s_%s_%s.log' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_min)
logfile = open('/home/pi/logs/' + logfilename, 'w')

#Log errors and other messages
def logerror(severity, e):
    if VERBOSITY >= severity:
        print(time.asctime() + ': ' + e, file=logfile)

#i2c commands
def i2c_simple_read(address):
    try:
        value = bus.read_byte(address)
        logerror(2, 'i2c SR addr=0x%02x OK val=0x%02x' % (address,value))
        return value
    except IOError:
        logerror(1, 'i2C SR addr=0x%02x IOError' % address)
        return None

def i2c_simple_write(address,value):
  try:
    bus.write_byte(address,value)
    logerror(2,'i2C SW addr=0x%02x val=0x%02x OK' % (address,value))
    return True
  except IOError:
    logerror(1,'i2C SW addr=0x%02x val=0x%02x IOError' % (address,value))
    return None

def i2c_complex_read(address,register,length):
  try:
    value = bus.read_i2c_block_data(address,register,length)
    logerror(2,'i2C SR addr=0x%02x reg=0x%02x OK val=0x%02x' \
                                                     % (address,register,value))
    return value
  except IOError:
    logerror(1,'i2C SR addr=0x%02x reg=0x%02x IOError' % (address,register))
    return None

def i2c_complex_write(address,register,value):
  try:
    bus.write_byte_data(address,register,value)
    logerror(2,'i2C SW addr=0x%02x reg=0x%02x val=0x%02x OK' \
                                                     % (address,register,value))
    return True
  except IOError:
    logerror(1,'i2C SW addr=0x%02x reg=0x%02x val=0x%02x IOError' \
                                                     % (address,register,value))
    return None

#message handling
def parseMessage(message):
    #procedure for parsing each command
    #Parse simple read
    def SR(match):
        addr = match.group(1)
        value = i2c_simple_read(int(addr,0))
        if (value != None):
            return(message + ' OK ' + hex(value))
        else:
            return(message + ' ER')
    #Parse simple write
    def SW(match):
        addr = match.group(1)
        value = match.group(2)
        ret = i2c_simple_write(int(addr,0),int(value,0))
        if (ret != None):
            return(message + ' OK')
        else:
            return(message + ' ER')

    #Parse complex read
    def CR(match):
        addr = match.group(1)
        register = match.group(2)
        ret = i2c_complex_read(int(addr,0),int(register,0),4)
        if (ret != None):
            formattedMessage = ' '.join([message, 'OK']+ret)
            return(formatterMessage)
        else:
            return(message + ' ER')

    #Parse complex write
    def CW(match):
        addr = match.group(1)
        register = match.group(2)
        value = match.group(3)
        ret = i2c_complex_write(int(addr,0),int(register,0),int(value,0))
        if (ret != None):
            return(message + ' OK')
        else:
            return(message + ' ER')

    #use regex to determine kind of message and execute
    cmds = {
            r"SR\s+(\w+)" :                 SR,
            r"SW\s+(\w+)\s+(\w+)" :         SW,
            r"CR\s+(\w+)\s+(\w+)":          CR,
            r"CW\s+(\w+)\s+(\w+)\s+(\w+)" : CW
            }

    for case, cmd in cmds.iteritems():
        match = re.search(case, message,re.I|re.X)
        if match:
            return cmd(match)
    return

#websocket
class WSHandler(tornado.websocket.WebSocketHandler):

    #connection established by client
    def open(self):
        logerror(2,'Connection Established')

    #message sent from client
    def on_message(self, message):
        logerror(2,'Received message: %s' % message)
        self.write_message(parseMessage(message))

    def on_close(self):
        logerror(2,'Connection Closed')

#prep server
application = tornado.web.Application([(r'/ws', WSHandler),])

#start server
if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(1738)
  tornado.ioloop.IOLoop.instance().start()
