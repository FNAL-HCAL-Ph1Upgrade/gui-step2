# This is the meat behind the testing suite. It is a culmination
# of everybody's individual codes. The main function of this code
# is to generate log functions regarding the tests being
# conducted.

from client import webBus
import QIELib
import testLib
import iglooTest
import json
import bridge_test
import vttxTest
from datetime import datetime
from qieCardClass import qieCard

class qieCommands:

	def __init__(self):	
		self.humiStore = -99.0
		self.tempStore = -99.0
		self.passesTemp = False
		self.passesHumi = False
		self.b = webBus("pi7")

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
		self.b.sleep(500)
		self.b.read(0x40,2)

		bigData = self.b.sendBatch()
		data = bigData[4]
		data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		#Converting the temperature using equation
		temp = (-46.85) +175.72*(data)/(2**16)
		self.tempStore = round(temp,3)

	def sensorHumid(self,rm,qieCard):  # Thanks, Adryanna!
		#b = webBus("pi5")
		self.b.write(0x00,[0x06])
		self.b.write(qieCard,[0x11,0x05,0,0,0])
		self.b.write(0x40,[0xf5])
		self.b.sleep(500)
		self.b.read(0x40,2)

		bigData = self.b.sendBatch()
		data = bigData[4]
		data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		#Converting the humidity using equation
		humid = -6 + 125.0*(data)/(2**16)
		self.humiStore = round(humid,3)

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

	def testVttx(self,card,webBus):
		self.vttx1Result = vttxTest.vttx1RWR(card, webBus)
		self.vttx2Result = vttxTest.vttx2RWR(card, webBus)
		 
		
#	def runSuiteCompForm(self,register, jsonFile, tester, logFile):
	def runSuiteCompForm(self,register,runNumber):

		resultsString = bridge_test.basicTests(register,27)
		
		# Information coming from the bridge tests
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
		self.testVttx(register,self.b)
		self.activeCard.thermOneWire = resultsString[26]
		self.activeCard.qieDaisyChn1 = resultsString[25]
		self.activeCard.qieDaisyChn0 = resultsString[24]
		self.activeCard.orbitHisto6  = resultsString[23]
		self.activeCard.orbitHisto5  = resultsString[22]
		self.activeCard.orbitHisto4  = resultsString[21]
		self.activeCard.orbitHisto3  = resultsString[20]
		self.activeCard.orbitHisto2  = resultsString[19]
		self.activeCard.orbitHisto1  = resultsString[18]
		self.activeCard.orbitHisto0  = resultsString[17]
		self.activeCard.controlReg   = resultsString[16]
		self.activeCard.igloo2Cntrl  = resultsString[15]
		self.activeCard.bkplnSpare3Counter = resultsString[14]
		self.activeCard.bkplnSpare2Counter = resultsString[13]
		self.activeCard.bkplnSpare1Counter = resultsString[12]
		self.activeCard.wteCounter = resultsString[11]
		self.activeCard.resQieCounter = resultsString[10]
		self.activeCard.clockCounter = resultsString[9]
		self.activeCard.scratch = resultsString[6]
		self.activeCard.onesZeros = resultsString[5]

		# Information coming from vtxxResults
		self.activeCard.vttx1Result = self.vttx1Result
		self.activeCard.vttx2Result = self.vttx2Result

		# Information coming from igloo 
		iglooTest.openIgloo(register)	
		self.activeCard.igloo_fpgaMajVer = iglooTest.fpgaMajVer()
		self.activeCard.igloo_fpgaMinVer = iglooTest.fpgaMinVer()
		self.activeCard.igloo_onesRegist = iglooTest.ones()
		self.activeCard.igloo_zeroRegist = iglooTest.zeros()
		self.activeCard.igloo_FPGAtopBot = iglooTest.FPGATopOrBottom()
		self.activeCard.igloo_uniqueID   = iglooTest.uniqueID()
		self.activeCard.igloo_statusReg  = iglooTest.statusReg()
		self.activeCard.igloo_cnterReg   = iglooTest.cntrReg()
		self.activeCard.igloo_clockCount = iglooTest.clk_count()
		self.activeCard.igloo_qieResetCount = iglooTest.rst_QIE_count()
		self.activeCard.igloo_wteCounter    = iglooTest.wte_count()
		self.activeCard.igloo_capIdErrorCnt = iglooTest.capIDErr_count()
		self.activeCard.igloo_fifoData      = iglooTest.fifo_data()
		self.activeCard.igloo_inputSpy      = iglooTest.inputSpy()
		self.activeCard.igloo_spy96bits     = iglooTest.spy96bits()
		self.activeCard.igloo_qie_clockPh   = iglooTest.qie_ck_ph()
		self.activeCard.igloo_linkTestMode  = iglooTest.link_test_mode()
		self.activeCard.igloo_linkTestPatt  = iglooTest.link_test_pattern()
		self.activeCard.igloo_SERDES_test   = iglooTest.SERDES()
		self.activeCard.igloo_scratchRegis  = iglooTest.scratchReg()

		with open(self.activeCard.uniqueID + ".log", 'a') as logFile:
			with open(self.activeCard.uniqueID +"_"+str(runNumber)+"_raw.json", 'w') as jsonFile:

				logFile.write("\nQIE Card being tested: "+str(hex(register)))
				logFile.write("\nUnique ID:  "+ str(self.activeCard.uniqueID))
				logFile.write("\nHerm test:  "+ str(self.activeCard.passedHerm))
				logFile.write("\nBrdg test:  "+ str(self.activeCard.passedBrdg))
				logFile.write("\nOnes Register:  "+ str(self.activeCard.passedOnes))
				logFile.write("\nZero Register:  "+ str(self.activeCard.passedZero))
				logFile.write("\n0's/1's Register: "+ self.activeCard.onesZeros)
				logFile.write("\nFirmware Ver.:  "+ self.activeCard.firmwareVer)
				logFile.write("\nTemperature: "   + str(self.activeCard.temperature))
				logFile.write("\nPasses Temp: "   + str(self.passesTemp))
				logFile.write("\nPasses Humi: "   + str(self.passesHumi))
				logFile.write("\nHumidity: "      + str(self.activeCard.humidity))
				logFile.write("\nTherm. One Wire: " + self.activeCard.thermOneWire)
				logFile.write("\nQIE Daisy Chain 0: " + self.activeCard.qieDaisyChn0)
				logFile.write("\nQIE Daisy Chain 1: " + self.activeCard.qieDaisyChn1)
				logFile.write("\nOrbit Histogram 0: " + self.activeCard.orbitHisto0)
				logFile.write("\nOrbit Histogram 1: " + self.activeCard.orbitHisto1)
				logFile.write("\nOrbit Histogram 2: " + self.activeCard.orbitHisto2)
				logFile.write("\nOrbit Histogram 3: " + self.activeCard.orbitHisto3)
				logFile.write("\nOrbit Histogram 4: " + self.activeCard.orbitHisto4)
				logFile.write("\nOrbit Histogram 5: " + self.activeCard.orbitHisto5)
				logFile.write("\nOrbit Histogram 6: " + self.activeCard.orbitHisto6)
				logFile.write("\nControl Reg: "       + self.activeCard.controlReg)
				logFile.write("\nigloo2 FPGA Cntrl: " + self.activeCard.igloo2Cntrl)
				logFile.write("\nBackplane Spare Counter 1: " + self.activeCard.bkplnSpare1Counter)
				logFile.write("\nBackplane Spare Counter 2: " + self.activeCard.bkplnSpare2Counter)
				logFile.write("\nBackplane Spare Counter 3: " + self.activeCard.bkplnSpare3Counter)
				logFile.write("\nWTE Counter: " + self.activeCard.wteCounter)
				logFile.write("\nRES_QIE Counter: " + self.activeCard.resQieCounter)
				logFile.write("\nClock Counter: " + self.activeCard.clockCounter)
				logFile.write("\nScratch Register: " + self.activeCard.scratch)
				logFile.write("\nAlternating (a's) Register: " + self.activeCard.onesZeros)
				logFile.write("\n\nVttx 1 Read: "   + self.activeCard.vttx1Result)
				logFile.write("\nVttx 2 Read: "   + self.activeCard.vttx2Result)
				logFile.write("\n\nData from Igloo Tests")
				logFile.write("\nFPGA Major Version: "+self.activeCard.igloo_fpgaMajVer)
         		        logFile.write("\nFPGA Minor Version: "+self.activeCard.igloo_fpgaMinVer)
		                logFile.write("\nOnes Register: "+self.activeCard.igloo_onesRegist)
               			logFile.write("\nZeros Register: "+self.activeCard.igloo_zeroRegist)
		                logFile.write("\nFPGA Top or Bottom: "+self.activeCard.igloo_FPGAtopBot)
		                logFile.write("\nIgloo Unique ID: "+self.activeCard.igloo_uniqueID)
    			        logFile.write("\nStatus Register: "+self.activeCard.igloo_statusReg)
                		logFile.write("\nCounter Register: "+self.activeCard.igloo_cnterReg)
                		logFile.write("\nClock Counter: "+self.activeCard.igloo_clockCount)
                		logFile.write("\nQIE Reset Counter: "+self.activeCard.igloo_qieResetCount)
                		logFile.write("\nWTE Counter: "+self.activeCard.igloo_wteCounter)
                		logFile.write("\nCap ID Error Counter: "+self.activeCard.igloo_capIdErrorCnt)
                		logFile.write("\nFIFO Data: "+self.activeCard.igloo_fifoData)
                		logFile.write("\nInput Spy: "+self.activeCard.igloo_inputSpy)
                		logFile.write("\nSpy 96 Bits: "+self.activeCard.igloo_spy96bits)
                		logFile.write("\nQIE Clock Phase: "+self.activeCard.igloo_qie_clockPh)
                		logFile.write("\nLink Test Mode: "+self.activeCard.igloo_linkTestMode)
                		logFile.write("\nLink Test Pattern: "+self.activeCard.igloo_linkTestPatt)
                		logFile.write("\nSERDES Test: "+self.activeCard.igloo_SERDES_test)
                		logFile.write("\nScratch Register: "+self.activeCard.igloo_scratchRegis)
				logFile.write("\n\nTests for "+str(hex(register))+" complete.")
				logFile.write("\n\n")

				json.dump(self.activeCard, jsonFile, default=self.jdefault)
	
	def runCompleteSuite(self,register,runNumber):
		self.runSuiteCompForm(register,runNumber)

#	def runCompleteSuite(self,register,humanFile,jsonFile,inTester,logFile):
#		self.runSuiteCompForm(register,jsonFile,inTester,logFile)
