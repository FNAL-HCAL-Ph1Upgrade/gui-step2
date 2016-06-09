# This is a file that contains some basic checks to run
# On QIE cards

from client import webBus
import QIELib
import testLib

def hermTest(register):
	b = webBus("pi5")
	b.write(register,[0x00])
	b.read(register, 4)
	outString = b.sendBatch()[1]
	outString = testLib.reverseBytes(outString)
	if (testLib.toASCII(outString) == "HERM"):
		return "PASS"
	else:
		return "FAIL"
		
def brdgTest(register):
	b = webBus("pi5")
	b.write(register,[0x01])
	b.read(register, 4)
	outString = b.sendBatch()[1]
	outString = testLib.reverseBytes(outString)
	if (testLib.toASCII(outString) == "Brdg"):
		return "PASS"
	else:
		return "FAIL"

def tff_Test(register):
	b = webBus("pi5")
	b.write(register,[0x08])
	b.read(register, 4)
	if (b.sendBatch()[1] == "255 255 255 255"):
		return "PASS"
	else:
		return "FAIL"

def zeroTest(register):
	b = webBus("pi5")
	b.write(register,[0x09])
	b.read(register, 4)
	if (b.sendBatch()[1] == "0 0 0 0"):
		return "PASS"
	else:
		return "FAIL"
	
def fwVerTest(register):
	b = webBus("pi5")
	b.write(register,[0x04])
	b.read(register, 4)
	return testLib.reverseBytes(b.sendBatch()[1])

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
	b.read(0x40,2)

	bigData = b.sendBatch()
	data = bigData[3]
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
	b.read(0x40,2)

	data = b.sendBatch()[3]
	data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
	#Converting the humidity using equation
	humid = -6 + 125.0*(data)/(2**16)
	humid = round(humid,3)
	return humid

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
	
def runSuite(register):
	# HUMAN-READABLE FORMAT
	# The weird parts of the following print statement
	# allow us to print colored font to the terminal.
	# Feel free to remove the colored font if it doesn't work.
	print '\033[93m'+"\nQIE Card being tested: "+'\033[0m','\033[96m'+str(hex(register))+'\033[0m'
	print "Unique ID:  ", str(getUniqueID(0,register))
	print "Herm test:  ", hermTest(register)
	print "Brdg test:  ", brdgTest(register)
	print "Ones Register:  ", tff_Test(register)
	print "Zero Register:  ", zeroTest(register)
	print "Firmware Ver.:  ", fwVerTest(register)
	print "Temperature: "   , sensorTemp(0,register), " C"
	print "Humidity: "      , sensorHumid(0,register)
	print "Overall Status: ", statusCheck(register)
	return "\nTests for "+str(register)+" complete."

def runSuiteCompForm(register, inFile):
	# COMPUTER-PARSING FORMAT
	inFile.write(str(hex(register))+"\n")
	inFile.write("UniqueID\n")
	inFile.write(str(getUniqueID(0,register))+"\n")
	inFile.write("Temp\n")
	inFile.write(str(sensorTemp(0,register))+"\n")
	inFile.write("Humi\n")
	inFile.write(str(sensorHumid(0,register))+"\n")
	inFile.write("Herm\n")
	inFile.write(str(hermTest(register))+"\n")
	inFile.write("Brdg\n")
	inFile.write(str(brdgTest(register))+"\n")
	inFile.write("Ones\n")
	inFile.write(str(tff_Test(register))+"\n")
	inFile.write("Zero\n")
	inFile.write(str(zeroTest(register))+"\n")
	inFile.write("Fver\n")
	if str(fwVerTest(register) == "1 11 0 0"):
		inFile.write("PASS\n")
	else:
		inFile.write("FAIL\n")




