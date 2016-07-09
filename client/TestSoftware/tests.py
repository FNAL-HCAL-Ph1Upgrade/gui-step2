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
import uHTR
import vttxLib
import temp
from Checksum import Check
import loggerClass as logClass

# Cutoff for card overheating. Hopefully they never get this hot...
# Degrees Celsius
tempThreshold = 55

# These dictionaries will be used to get information from
# the card that pertains to UID, Temperature, and Humidity
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
	print 'DEBUG... Iterations: ' +str(i)

	# Info for logfiles
	self.fileName = sys.stdout.name
	self.backupStdout = sys.stdout

	# Using the listOfTests.py file, initialize our test suites.
	self.registers = listOfTests.initializeBridgeList(self.b, self.a, i)
	self.iglooRegs = listOfTests.initializeIglooList(self.b, self.a, i)
	self.vttxRegs_1  = listOfTests.initializeVttxList_1(self.b, self.a, i)
	self.vttxRegs_2  = listOfTests.initializeVttxList_2(self.b, self.a, i)
	self.longRegs  = listOfTests.initializeLongTests(self.b, self.a, i)

#######################################################################################

    # This function is used for getting stuff like temp., humid., and UID
    def readNoCheck(self, testName, iterations = 1):
	# Assign some names for read/write parameters
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
		# Switch to the proper i2c channel
		self.b.write(self.a,i2c_pathway)
		# Send command to the active register
		self.b.write(register,command)
		if (napTime != 0):
			self.b.sleep(napTime)  #catching some z's
		# Read back what we actually want
		self.b.read(register,size)

	# Process the above read/write commands
	r = self.b.sendBatch()
	# Remove the entries in r that contain no information
	for i in r:
		if (i != '0' and i != 'None'):
			new_r.append(i)

	self.outCard.cardGenInfo[testName] = new_r
	
	# Do things that depend on whether we're getting UID or Temp/Humid
	if (testName == "Unique_ID"):
		message = r[-1]
		check = Check(message,0)
		# Using checksum, ask: is the message "good"?
		if (check.result != 0):  # Message bad: print error, assign error UID.
			print 'Unique ID checksum error! Continuing...'
			self.outCard.cardGenInfo[testName] = "0xXXXXXXXXXXXXX"
		else:   # Message good: assign the card its UID.
			new_r[0] = helpers.reverseBytes(new_r[0])
			new_r[0] = helpers.toHex(new_r[0])
			self.outCard.cardGenInfo[testName]=new_r[0]

	elif (testName == "Temperature" or testName == "Humidity"):
		self.outCard.cardGenInfo[testName] = temp.readManyTemps(self.a,15,testName,"nohold")

################################################################################################

    def openIgloo(self, slot):
	#the igloo is value "3" in I2C_SELECT table
	self.b.write(0x00,[0x06])
	self.b.write(slot,[0x11,0x03,0,0,0])
	self.b.sendBatch()

    def openVTTX(self, slot, vttxNum):
	self.b.write(0x00,[0x06])
	if (vttxNum == 1):
    		self.b.write(slot,[0x11, 0x01, 0, 0, 0])
	elif (vttxNum == 2):
		self.b.write(slot,[0x11, 0x02, 0, 0, 0])
    	self.b.sendBatch()

##################################################################################################

    # The following function is for when we want to run ALL
    # tests on ALL active cards.
    def runTests(self, suite):
	self.JSlot = self.outCard.cardGenInfo["JSlot"]
	if (suite == "main" or suite == "bridge" or suite =="short"):
		# Immediately quit tests if the card gets too hot
		if (temp.readManyTemps(self.a,5,"Temperature","nohold") >= tempThreshold):
			return None
		print '-------------------------'
		print 'Running register tests!'
		print '-------------------------'
		# Loop over all basic register tests. Add the passes to the [0] index. Add the fails to the [1] index
		for r in self.registers.keys():
			sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
			results = self.registers[r].run()
			self.outCard.resultList[r][0] += results[0]
			self.outCard.resultList[r][1] += results[1]
			print r+" tests completed."
			strReturn = sys.stdout.strReturn
			strReturn = strReturn.replace("\n","\\n")
			self.outCard.bridgeResults[r]='"'+strReturn+'"'

		sys.stdout = self.backupStdout

	if (suite == "main" or suite == "igloo" or suite == "short"):
		# Immediately quit tests if the card gets too hot
		if (temp.readManyTemps(self.a,5,"Temperature","nohold") >= tempThreshold):
			return None
		self.openIgloo(self.a)
		print '\n-------------------------'
		print 'Running IGLOO tests!'
		print '-------------------------'
		# Loop over all igloo tests. Add the passes to the [0] index. Add the fails to the [1] index
		for r in self.iglooRegs.keys():
			sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
			print r
			results = self.iglooRegs[r].run()
			self.outCard.iglooList[r][0] += results[0]
			self.outCard.iglooList[r][1] += results[1]
			print r+" tests completed."
			strReturn = sys.stdout.strReturn
			strReturn = strReturn.replace("\n","\\n")
			self.outCard.iglooResults[r]='"'+strReturn+'"'

		self.stdout = self.backupStdout

	if (suite == "main" or suite == "vttx" or suite == "short"):
		# Immediately quit tests if the card gets too hot
		if (temp.readManyTemps(self.a,5,"Temperature","nohold") >= tempThreshold):
			return None
		self.openVTTX(self.a, 1)
		print '\n-------------------------'
		print 'Running VTTX_1 tests!'
		print '-------------------------'
		# Loop over all vttx tests. Add the passes to the [0] index. Add the fails to the [1] index
		for r in self.vttxRegs_1.keys():
			sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
			results = self.vttxRegs_1[r].run()
			self.outCard.vttxListOne[r][0] += results[0]
			self.outCard.vttxListOne[r][1] += results[1]
			print r+" tests completed."
			strReturn = strReturn
			strReturn = strReturn.replace("\n","\\n")
			self.outCard.vttxOneResults[r]='"'+strReturn+'"'

		self.stdout = self.backupStdout

		# Immediately quit tests if the card gets too hot
		if (temp.readManyTemps(self.a,5,"Temperature","nohold") >= tempThreshold):
			return None
		self.openVTTX(self.a, 2)
		print '\n-------------------------'
		print 'Running VTTX_2 tests!'
		print '-------------------------'
		# Loop over all vttx tests. Add the passes to the [0] index. Add the fails to the [1] index
		for r in self.vttxRegs_2.keys():
			sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
			results = self.vttxRegs_2[r].run()
			self.outCard.vttxListTwo[r][0] += results[0]
			self.outCard.vttxListTwo[r][1] += results[1]
			print r+" tests completed."
			strReturn = sys.stdout.strReturn
			strReturn = strReturn.replace("\n","\\n")
			self.outCard.vttxTwoResults[r]='"'+strReturn+'"'

		self.stdout = self.backupStdout

	if (suite == "main" or suite == "long"):
		# Immediately quit tests if the card gets too hot
		if (temp.readManyTemps(self.a,5,"Temperature","nohold") >= tempThreshold):
			return None
		print '\n-------------------------'
		print 'Running long tests!'
		print '-------------------------'
		# Loop over all long, involved tests. Add the passes to the [0] index. Add the fails to the [1] index
		for r in self.longRegs.keys():
			# If we're doing the inputspy test, we need to open the igloo ahead of time
			if (r == "OrbitHistograms"):
				sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
			elif (r == "inputSpy_512Reads"):
				self.openIgloo(self.a)
			results = self.longRegs[r].run()
			self.outCard.longTestList[r][0] += results[0]
			self.outCard.longTestList[r][1] += results[1]
			print r+" tests completed."
			if (r == "OrbitHistograms"):
				strReturn = sys.stdout.strReturn
				strReturn = strReturn.replace("\n","\\n")
				self.outCard.longTestResults[r]='"'+strReturn+'"'

		self.stdout = self.backupStdout

	for r in noCheckRegis.keys():
	    self.readNoCheck(r, 1)

	
	sys.stdout = logClass.loggerSingleTest(self.fileName, str(self.JSlot))
	self.outCard.printResults()
	sys.stdout = self.backupStdout
	print '\n\n'
	self.outCard.writeMachineJson()

#############################################################################################################

    def runSingleTest(self,key):
	if key in registers:
		yield self.readWithCheck(key, 100)
	elif key in noCheckRegis:
		yield self.readNoCheck(key, 1)
