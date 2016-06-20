#import helpers as h
from __future__ import print_function as logprint
import sys
sys.path.append('../')
import client
#from registers import registers

registers = {
    "ID_string" :{
        "address" : 0x00,
        "size" : 32,
        "RW" : 0,
        "expected" : "77 82 69 72" #MREH in ascii
        },
    "ID_string_cont" :{
        "address" : 0x01,
        "size" : 32,
        "RW" : 0,
        "expected" : "103 100 114 66" #gdrB in ascii
        },
    "Ones" :{
        "address" : 0x08,
        "size" : 32,
        "RW" : 0,
        "expected" : "255 255 255 255"
        },
    "Zeroes" :{
        "address" : 0x09,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 0 0 0"
        },
    "OnesZeroes" :{
        "address" : 0x0A,
        "size" : 32,
        "RW" : 0,
        "expected" : "170 170 170 170"
        }
}


class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logstream
        self.iterations = iterations
    def run(self):
        passes = 0
        for i in xrange(iterations):
            if self.testBody() == true: passes += 1
        return (passes, fails)
    def log(self, message):
        logprint(message, file=self.logfile)
    def testBody(self):
        return True

class testSuite:
    def __init__(self, webAddress, address):
        '''create a new test suite object... initialize bus and address'''
        self.bus = client.webBus(webAddress, 0)
        self.address = address

    #For basic read checks
    def readWithCheck(self, registerName, iterations = 1):
        passes = 0
        register = registers[registerName]["address"]
        size = 4#registers[registerName]["size"] / 8
        check = registers[registerName]["expected"]

        for i in xrange(iterations):
            self.bus.write(self.address, [register])
            self.bus.read(self.address, size)
        r = self.bus.sendBatch()
        for i in xrange(iterations * 2):
            if (i % 2 == 1) and (r[i] == check):
                passes += 1
        return (passes, iterations - passes) #(passes, fails)

    def runTests(self):
        for r in registers.keys():
            yield self.readWithCheck(r, 100)

    # for i in xrange(iterations):
    #     bus.read
    # return (passes, iterations - passes) #passes, fails
