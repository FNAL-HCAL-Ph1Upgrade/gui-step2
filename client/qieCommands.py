# This is a file that contains some basic checks to run
# On QIE cards

from client import webBus
import QIELib
import testLib
import json
from datetime import datetime
from qieCardClass import qieCard

class qieCommands:

	def __init__(self):	
		self.humiStore = -99.0
		self.tempStore = -99.0
		self.passesTemp = False
		self.passesHumi = False
		self.b = webBus("pi5")

	def jdefault(self,o):
		return o.__dict__

	def hermTest(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x00])
		self.b.read(register, 4)
		outString = self.b.sendBatch()[1]
		outString = testLib.reverseBytes(outString)
		if (testLib.toASCII(outString) == "HERM"):
			return True
		else:
			return False
			
	def brdgTest(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x01])
		self.b.read(register, 4)
		outString = self.b.sendBatch()[1]
		outString = testLib.reverseBytes(outString)
		if (testLib.toASCII(outString) == "Brdg"):
			return True
		else:
			return False

	def tff_Test(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x08])
		self.b.read(register, 4)
		if (self.b.sendBatch()[1] == "255 255 255 255"):
			return  True
		else:
			return False

	def zeroTest(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x09])
		self.b.read(register, 4)
		if (self.b.sendBatch()[1] == "0 0 0 0"):
			return True
		else:
			return False
		
	def fwVerTest(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x04])
		self.b.read(register, 4)
		outString = self.b.sendBatch()[1]
		outString = testLib.reverseBytes(outString)

	def statusCheck(self,register):
		#b = webBus("pi5")
		self.b.write(register,[0x10])
		self.b.read(register, 4)
		return self.b.sendBatch()[1]

	def sensorTemp(self,rm,qieCard):    # Thanks, Adryanna!
		#b = webBus("pi5")
		self.b.write(0x00,[0x06])
		self.b.write(qieCard,[0x11,0x05,0,0,0])
		self.b.write(0x40,[0xf3])
		self.b.sleep(300)
		self.b.read(0x40,2)

		bigData = self.b.sendBatch()
		data = bigData[4]
		data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		#Converting the temperature using equation
		temp = (-46.85) +175.72*(data)/(2**16)
		self.tempStore = round(temp,3)
		print self.tempStore

	def sensorHumid(self,rm,qieCard):  # Thanks, Adryanna!
		#b = webBus("pi5")
		self.b.write(0x00,[0x06])
		self.b.write(qieCard,[0x11,0x05,0,0,0])
		self.b.write(0x40,[0xf5])
		self.b.sleep(300)
		self.b.read(0x40,2)

		bigData = self.b.sendBatch()
		data = bigData[4]
		data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		#Converting the humidity using equation
		humid = -6 + 125.0*(data)/(2**16)
		self.humiStore = round(humid,3)
		print self.humiStore

	def getUniqueID(self,rm, qieCard):  # Thanks, Caleb!
		#b = webBus("pi5")
		self.b.write(0x00,[0x06])
		self.b.write(qieCard,[0x11,0x04,0,0,0])
		self.b.write(0x50,[0x00])
		self.b.read(0x50,8)
		raw_bus = self.b.sendBatch()
		cooked_bus = testLib.reverseBytes(raw_bus[-1])
		cooked_bus = testLib.serialNum(cooked_bus)
		return(testLib.toHex(cooked_bus))

	def temperatureTest(self):
		if (self.tempStore < 45 and self.tempStore > 10):
			self.passesTemp = True
		else:
			self.passesTemp = False

	def humidityTest(self):
		if (self.humiStore < 50 and self.humiStore > 0):
			self.passesHumi = True
		else:
			self.passesHumi = False
		 
		
#	def runSuiteCompForm(self,register, jsonFile, tester, logFile):
	def runSuiteCompForm(self,register,runNumber):

		self.activeCard = qieCard()
		self.activeCard.timeOfTest = str(datetime.now())
		#self.activeCard.tester = tester
		self.activeCard.i2cAddress = str(hex(register))
		self.activeCard.uniqueID = str(self.getUniqueID(0,register))
		self.sensorTemp(0,register)
		self.sensorHumid(0,register)
		self.activeCard.temperature = self.tempStore
		self.activeCard.humidity = self.humiStore
		self.temperatureTest()
		self.humidityTest()
		self.activeCard.passedTemp = self.passesTemp
		self.activeCard.passedHumid = self.passesHumi
		self.activeCard.firmwareVer = str(self.fwVerTest(register))
		self.activeCard.passedHerm = self.hermTest(register)
		self.activeCard.passedBrdg = self.brdgTest(register)
		self.activeCard.passedOnes = self.tff_Test(register)
		self.activeCard.passedZero = self.zeroTest(register)

		with open(self.activeCard.uniqueID + ".log", 'a') as logFile:
			with open(self.activeCard.uniqueID +"_"+str(runNumber)+"_raw.json", 'w') as jsonFile:

				logFile.write("\nQIE Card being tested: "+str(hex(register)))
				logFile.write("\nUnique ID:  "+ str(self.activeCard.uniqueID))
				logFile.write("\nHerm test:  "+ str(self.activeCard.passedHerm))
				logFile.write("\nBrdg test:  "+ str(self.activeCard.passedBrdg))
				logFile.write("\nOnes Register:  "+ str(self.activeCard.passedOnes))
				logFile.write("\nZero Register:  "+ str(self.activeCard.passedZero))
				logFile.write("\nFirmware Ver.:  "+ self.activeCard.firmwareVer)
				logFile.write("\nTemperature: "   + str(self.activeCard.temperature))
				logFile.write("\nPasses Temp: "   + str(self.passesTemp))
				logFile.write("\nPasses Humi: "   + str(self.passesHumi))
				logFile.write("\nHumidity: "      + str(self.activeCard.humidity))
				logFile.write("\n\nTests for "+str(hex(register))+" complete.")
				logFile.write("\n\n")

				json.dump(self.activeCard, jsonFile, default=self.jdefault)
	
	def runCompleteSuite(self,register,runNumber):
		self.runSuiteCompForm(register,runNumber)

#	def runCompleteSuite(self,register,humanFile,jsonFile,inTester,logFile):
#		self.runSuiteCompForm(register,jsonFile,inTester,logFile)
