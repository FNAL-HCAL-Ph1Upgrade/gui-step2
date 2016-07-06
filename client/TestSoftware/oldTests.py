#import helpers as h
import sys
import inspect
#sys.path.append('../')
from testSummary import testSummary
import bridgeTests
import client
import helpers
import Test
#from registers import registers

registers = {
    "ID_string" :{
        "address" : 0x00,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 77 82 69 72" #MREH in ascii
        },
    "ID_string_cont" :{
        "address" : 0x01,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 103 100 114 66" #gdrB in ascii
        },
    "Ones" :{
        "address" : 0x08,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 255 255 255 255" #0xFFFFFFFF in hex
        },
    "Zeroes" :{
        "address" : 0x09,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 0 0 0 0"
        },
    "OnesZeroes" :{
        "address" : 0x0A,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 170 170 170 170" #0xAAAAAAAA in hex
        },
    "Firmware_Ver" :{
	"address" : 0x04,
	"size" : 32,
	"RW" : 1,
	"expected" : "0 0 0 11 01"
	}
}

noCheckRegis = {
	"Unique_ID" :{
		"i2c_path" : [0x11, 0x04, 0,0,0],
		"address" : 0x50,
		"command" : [0x00],
		"sleep" : 0,
		"size" : 64,
		"RW" : 0,
#		"spaces" : 3
	},
	"Temperature" : {
		"i2c_path" : [0x11, 0x05, 0,0,0],
		"address" : 0x40,
		"command" : [0xf3],
		"sleep" : 300,
		"size" : 16,
		"RW" : 0
	},
	"Humidity" : {
		"i2c_path" : [0x11, 0x05, 0,0,0],
		"address" : 0x40,
		"command" : [0xf5],
		"sleep" : 300,
		"size" : 16,
		"RW" : 0
	}
}

class testSuite:
    def __init__(self, webAddress, address):
        '''create a new test suite object... initialize bus and address'''
        self.bus = client.webBus(webAddress, 0)
        self.address = address
	self.outCard = testSummary()

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
        self.outCard.resultList[registerName] = (passes, iterations - passes) #(passes, fails)
	return (passes, iterations - passes)

    def readNoCheck(self, testName, iterations = 1):
	i2c_pathway = noCheckRegis[testName]["i2c_path"]
	register = noCheckRegis[testName]["address"]
	size = noCheckRegis[testName]["size"]/8
	command = noCheckRegis[testName]["command"]
	napTime = noCheckRegis[testName]["sleep"]

	for i in xrange(iterations):
		# Clear the backplane
		self.bus.write(0x00,[0x06])

		self.bus.write(self.address,i2c_pathway)
		self.bus.write(register,command)
		if (napTime != 0):
			self.bus.sleep(napTime)  #catching some z's
		self.bus.read(register,size)

	r = self.bus.sendBatch()
	# Remove the entries in r that contain no information
	new_r = []
	for i in r:
		if (i != '0' and i != 'None'):
			new_r.append(i)
	self.outCard.resultList[testName] = new_r
	if (testName == "Unique_ID"):
		new_r[0] = helpers.reverseBytes(new_r[0])
		new_r[0] = helpers.toHex(new_r[0])
	return new_r

#   def runTests(self,barcode):
    def runTests(self):
	print inspect.getmembers(Test)
        for r in registers.keys():
            self.readWithCheck(r, 100)
	for r in noCheckRegis.keys():
	    self.readNoCheck(r, 1)
#	self.outCard.resultList["Barcode"]=barcode
	self.outCard.printResults()
	print "\n\n"
	self.outCard.writeHumanLog()
	self.outCard.writeMachineJson()

    def runSingleTest(self,key):
	if key in registers:
		yield self.readWithCheck(key, 100)
	elif key in noCheckRegis:
		yield self.readNoCheck(key, 1)
