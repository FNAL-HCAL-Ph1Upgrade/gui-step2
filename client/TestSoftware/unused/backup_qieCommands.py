# This is a file that contains some basic checks to run
# On QIE cards

from client import webBus
import QIELib
import testLib
import json
from datetime import datetime
from qieCardClass import qieCard

tempStore = -99.0
humiStore = -99.0

def jdefault(o):
	return o.__dict__

def hermTest(register):
	b = webBus("pi5")
	b.write(register,[0x00])
	b.read(register, 4)
	outString = b.sendBatch()[1]
	outString = testLib.reverseBytes(outString)
	if (testLib.toASCII(outString) == "HERM"):
		return True
	else:
		return False
		
def brdgTest(register):
	b = webBus("pi5")
	b.write(register,[0x01])
	b.read(register, 4)
	outString = b.sendBatch()[1]
	outString = testLib.reverseBytes(outString)
	if (testLib.toASCII(outString) == "Brdg"):
		return True
	else:
		return False

def tff_Test(register):
	b = webBus("pi5")
	b.write(register,[0x08])
	b.read(register, 4)
	if (b.sendBatch()[1] == "255 255 255 255"):
		return  True
	else:
		return False

def zeroTest(register):
	b = webBus("pi5")
	b.write(register,[0x09])
	b.read(register, 4)
	if (b.sendBatch()[1] == "0 0 0 0"):
		return True
	else:
		return False
	
def fwVerTest(register):
	b = webBus("pi5")
	b.write(register,[0x04])
	b.read(register, 4)
	outString = b.sendBatch()[1]
	outString = testLib.reverseBytes(outString)

def statusCheck(register):
	b = webBus("pi5")
	b.write(register,[0x10])
	b.read(register, 4)
	return b.sendBatch()[1]

def sensorTemp(rm,qieCard):    # Thanks, Adryanna!
	b = webBus("pi5")
	b.write(0x00,[0x06])
	b.write(qieCard,[0x11,0x05,0,0,0])
	b.write(0x40,[0xf3])
	b.sleep(300)
	b.read(0x40,2)

	bigData = b.sendBatch()
	data = bigData[4]
	data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
	#Converting the temperature using equation
	temp = (-46.85) +175.72*(data)/(2**16)
	temp = round(temp,3)
	return temp

def sensorHumid(rm,qieCard):  # Thanks, Adryanna!
	b = webBus("pi5")
	b.write(0x00,[0x06])
	b.write(qieCard,[0x11,0x05,0,0,0])
	b.write(0x40,[0xf5])
	b.sleep(300)
	b.read(0x40,2)

	bigData = b.sendBatch()
	data = bigData[4]
	data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
	#Converting the humidity using equation
	humid = -6 + 125.0*(data)/(2**16)
	humiStore = round(humid,3)
#	return humiStore

def getUniqueID(rm, qieCard):  # Thanks, Caleb!
	b = webBus("pi5")
	b.write(0x00,[0x06])
	b.write(qieCard,[0x11,0x04,0,0,0])
	b.write(0x50,[0x00])
	b.read(0x50,8)
	raw_bus = b.sendBatch()
	cooked_bus = testLib.reverseBytes(raw_bus[-1])
	cooked_bus = testLib.serialNum(cooked_bus)
	return(testLib.toHex(cooked_bus))

#def temperatureTest(temp):
	 
	
def runSuite(register, inFile):
	# HUMAN-READABLE FORMAT
	# The weird parts of the following print statement
	# allow us to print colored font to the terminal.
	# Feel free to remove the colored font if it doesn't work.
	inFile.write("\nQIE Card being tested: "+str(hex(register)))
	inFile.write("\nUnique ID:  "+ str(getUniqueID(0,register)))
	inFile.write("\nHerm test:  "+ str(hermTest(register)))
	inFile.write("\nBrdg test:  "+ str(brdgTest(register)))
	inFile.write("\nOnes Register:  "+ str(tff_Test(register)))
	inFile.write("\nZero Register:  "+ str(zeroTest(register)))
	inFile.write("\nFirmware Ver.:  "+ str(fwVerTest(register)))
	inFile.write("\nTemperature: "   + str(sensorTemp(0,register))+" C")
	inFile.write("\nHumidity: "      + str(sensorHumid(0,register)))
	inFile.write("\nOverall Status: "+ statusCheck(register))
	inFile.write("\n\nTests for "+str(hex(register))+" complete.")

def runSuiteCompForm(register, inFile, tester):
	# COMPUTER-PARSING FORMAT
	activeCard = qieCard()
	activeCard.timeOfTest = str(datetime.now())
	activeCard.tester = tester
	activeCard.i2cAddress = str(hex(register))
	activeCard.uniqueID = str(getUniqueID(0,register))
	activeCard.temperature = sensorTemp(0,register)
#	activeCard.humidity = sensorHumid(0,register)
	activeCard.humidity = humiStore
	activeCard.firmwareVer = str(fwVerTest(register))
	activeCard.passedHerm = hermTest(register)
	activeCard.passedBrdg = brdgTest(register)
	activeCard.passedOnes = tff_Test(register)
	activeCard.passedZero = zeroTest(register)
	json.dump(activeCard, inFile, default=jdefault)

def runCompleteSuite(register,humanFile,machineFile,inTester):
	runSuite(register,humanFile)
	runSuiteCompForm(register,machineFile,inTester)
