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
import sys
import time
import re

#For i2c
import py2c

#setup
VERBOSITY = 2
bus = py2c.Bus()
t = time.localtime()
logfilename = '%s_%s_%s_%s.log' % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_min)
logfile = open('/home/pi/logs/' + logfilename, 'w')


#redirect to log file
sys.stdout = logfile
#Log errors and other messages
def logerror(severity, e):
    if VERBOSITY >= severity:
        print(time.asctime() + ': ' + e, file=logfile)

#i2c commands

#address is an int (hex is helpful)
#returns a list of length numbytes
def read(address, numbytes):
    values = bus.i2c_read(address, numbytes)
    return ' '.join([str(i) for i in values])

#address is an int (hex is helpful)
#bytearray is a list of bytes to be written
def write(address, byteArray):
    return bus.i2c_write(address, byteArray)

#Waits a given number of microseconds
def sleep(n):
    bus.wait(n)

def parseMessage(m):
    message = m.split()
    if message[0].lower() == 'r':
        #read
        print(message)
        return read(int(message[1]), int(message[2]))
    elif message[0].lower() == 'w':
        #write
        arr = [int(i) for i in message[2:]]
        print(arr)
        return write(int(message[1]), arr)
    elif message[0].lower() == 's':
        #sleep
        sleep(message[1])
        return None

#websocket
class WSHandler(tornado.websocket.WebSocketHandler):

    #connection established by client
    def open(self):
        logerror(2,'Connection Established')

    #message sent from client
    def on_message(self, message):
        logerror(2,'Received message: %s' % message)
        ms = message.split('|')
        rets = []
        for m in ms:
            rets.append(str(parseMessage(m)))
        #o = '|'.join(rets)
        self.write_message('|'.join(rets))

    def on_close(self):
        logerror(2,'Connection Closed')

#prep server
application = tornado.web.Application([(r'/ws', WSHandler),])

#start server
if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(1738)
  tornado.ioloop.IOLoop.instance().start()

