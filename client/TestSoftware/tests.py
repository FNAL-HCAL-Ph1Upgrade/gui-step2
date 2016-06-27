import sys
from datetime import datetime
import inspect
import testSummary
import bridgeTests as bt
import vttxClass as vc
import iglooClass as ic
import client
import helpers
import Test
import listOfTests
import vttxLib
import temp
from checksumClass import Checksum

# These dictionaries will be used to get information from
# the card that isn't necessarily related to a "test" per se
noCheckRegis = {
	"Unique_ID" :{
		"i2c_path" : [0x11, 0x04, 0,0,0],
		"address" : 0x50,
		"command" : [0x00],
		"sleep" : 0,
		"size" : 64,
		"RW" : 0,
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
    def __init__(self, webAddress, address, inSummary, iters):
        '''create a new test suite object... initialize bus and address'''
        self.b = webAddress
	self.outCard = inSummary
        self.a = address
	i = iters

	# Using the listOfTests.py file, initialize our test suites.
	self.registers = listOfTests.initializeBridgeList(self.b, self.a, i)
	self.iglooRegs = listOfTests.initializeIglooList(self.b, self.a, i)
	self.vttxRegs_1  = listOfTests.initializeVttxList_1(self.b, self.a, i)
	self.vttxRegs_2  = listOfTests.initializeVttxList_2(self.b, self.a, i)

    # This function is used for getting stuff like temp., humid., and UID
    def readNoCheck(self, testName, iterations = 1):
	self.outCard.cardGenInfo["DateRun"] = str(datetime.now())
	i2c_pathway = noCheckRegis[testName]["i2c_path"]
	register = noCheckRegis[testName]["address"]
	size = noCheckRegis[testName]["size"]/8
	command = noCheckRegis[testName]["command"]
	napTime = noCheckRegis[testName]["sleep"]
	new_r = []

	for i in xrange(iterations):
		# Clear the backplane
		self.b.write(0x00,[0x06])
		self.b.write(self.a,i2c_pathway)
		self.b.write(register,command)
		if (napTime != 0):
			self.b.sleep(napTime)  #catching some z's
		self.b.read(register,size)

	r = self.b.sendBatch()
	# Remove the entries in r that contain no information
	for i in r:
		if (i != '0' and i != 'None'):
			new_r.append(i)

	self.outCard.cardGenInfo[testName] = new_r
	
	# Do things that depend on whether we're getting UID or Temp/Humid
	if (testName == "Unique_ID"):
		message = r[-1]
		check = Checksum(message,0)
		if (check.result != 0):
			print "Unique ID checksum error! Continuing..."
			self.outCard.cardGenInfo[testName] = "0xXXXXXXXXXXXXX"
		else:
			new_r[0] = helpers.reverseBytes(new_r[0])
			new_r[0] = helpers.toHex(new_r[0])
			self.outCard.cardGenInfo[testName]=new_r[0]
	elif (testName == "Temperature" or testName == "Humidity"):
								      #(address, iterations, "Temperature"/"Humidity","hold"/"nohold")
		self.outCard.cardGenInfo[testName] = temp.readManyTemps(self.a,15,testName,"nohold")

    def openIgloo(self, slot):
		#the igloo is value "3" in I2C_SELECT table
		self.b.write(slot,[0x11,0x03,0,0,0])
		self.b.sendBatch()

    def openVTTX(self, slot, vttxNum):
    	self.b.write(slot,[0x11] + vttxLib.vttx["i2c_select"][vttxNum])
    	self.b.sendBatch()


    # The following function is for when we want to run ALL
    # tests on ALL active cards.
    def runTests(self, suite):

	if (suite == "main" or suite == "bridge"):
		print "-------------------------"
		print "Running register tests!"
		print "-------------------------"
		for r in self.registers.keys():
			results = self.registers[r].run()
			self.outCard.resultList[r][0] += results[0]
			self.outCard.resultList[r][1] += results[1]
			print r+" tests completed."

	if (suite == "main" or suite == "igloo"):
		self.openIgloo(self.a)
		print "\n-------------------------"
		print "Running IGLOO tests!"
		print "-------------------------"
		for r in self.iglooRegs.keys():
			print r
			results = self.iglooRegs[r].run()
			self.outCard.iglooList[r][0] += results[0]
			self.outCard.iglooList[r][1] += results[1]
			print r+" tests completed."

	if (suite == "main" or suite == "vttx"):
		self.openVTTX(self.a, 1)
		print "\n-------------------------"
		print "Running VTTX_1 tests!"
		print "-------------------------"
		for r in self.vttxRegs_1.keys():
			results = self.vttxRegs_1[r].run()
			self.outCard.vttxListOne[r][0] += results[0]
			self.outCard.vttxListOne[r][1] += results[1]
			print r+" tests completed."

		self.openVTTX(self.a, 2)
		print "\n-------------------------"
		print "Running VTTX_2 tests!"
		print "-------------------------"
		for r in self.vttxRegs_2.keys():
			results = self.vttxRegs_2[r].run()
			self.outCard.vttxListTwo[r][0] += results[0]
			self.outCard.vttxListTwo[r][1] += results[1]
			print r+" tests completed."

	for r in noCheckRegis.keys():
	    self.readNoCheck(r, 1)

	self.outCard.printResults()
	print "\n\n"
	self.outCard.writeHumanLog()
	self.outCard.writeMachineJson()

    def runSingleTest(self,key):
	if key in registers:
		yield self.readWithCheck(key, 100)
	elif key in noCheckRegis:
		yield self.readNoCheck(key, 1)
