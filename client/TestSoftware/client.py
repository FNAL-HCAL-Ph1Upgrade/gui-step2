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
        self.VERBOSITY = VERBOSITY
        self.messages = []
        a = "ws://%s:1738/ws" % serverAddress
        self.ws = create_connection(a)

    def read(self, address, numbytes):
        m = "r %i %i" % (address, numbytes)
        self.messages.append(m)

    def write(self, address, byteArray):
        m = "w %i " % address
        for h in byteArray:
            m += str(h) + " "
        self.messages.append(m)
    def sleep(self, n):
        m = "s %i" % n
        self.messages.append(m)
    def sendBatch(self):
        self.ws.send('|'.join(self.messages))
        ret = self.ws.recv().split('|')
        if self.VERBOSITY >= 1:
            for e in xrange(len(self.messages)):
                print 'SENT: %s' % self.messages[e]
                print 'RECEIVED: %s' % ret[e]
        self.messages = []
        return ret

################################################################################
if __name__ == "__main__":
    print 'What you just ran is a library. Correct usage is to import this file\
    and use its class(es) and functions.'
