#!/usr/bin/python
#
#client.py
#client /library/ with which to send commands to server

#websocket (install websocket-client)
from websocket import create_connection

################################################################################
# webBus class
################################################################################

class webBus:
    def __init__(self, serverAddress = "pi5", VERBOSITY = 2):
        self.messages = []
        self.ws = create_connection("ws://%s:1738/ws") % serverAddress

    def read(self, address, numbytes):
        self.messages.append("r %i %i") % (address, numbytes)
    def write(self, address, byteArray):
        m = "w %i " % address
        for h in byteArray:
            m += str(h)
        self.messages.append(m)
    def sleep(self, n):
        self.messages.append("s %i") % n
    def sendBatch(self, messages):
        self.ws.send('|'.join(messages))
        ret = self.ws.recv().split('|')
        if VERBOSITY >= 1:
            for e in xrange(len(messages)):
                print "SENT: %s" % messages[e]
                print "RECEIVED: %s" % ret[e]
        return ret


################################################################################
if __name__ == "__main__":
    print "What you just ran is a library. Correct usage is to import this file\
    and use its class(es) and functions."

