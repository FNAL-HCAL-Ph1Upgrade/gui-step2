# This is a test class that will be the bridge
# between Jordan's code and the log files.

class testSummary:
	def __init__(self, summaryNo, logFile, overwrite):
		self.idNo = summaryNo

		self.cardGenInfo = {"Unique_ID" : "", "DateRun" : [], "User" : "", "JSlot" : -99,
				    "HumanLogFile" : "", "Overwrite" : False
		}

		self.resultList = {
			"ID_string" : [0,0], "ID_string_cont" : [0,0], "Ones" : [0,0],
			"Zeroes" : [0,0], "OnesZeroes" : [0,0], "Firmware_Ver" : [0,0],
			"Status" : [0,0], "TempPass" : [0,0], "HumiPass" : [0,0],
			"Scratch" : [0,0], "ClockCnt" : [0,0], "QIECount" : [0,0],
			"WTECount" : [0,0], "zeroOrbits" : [0,0]
		}

		self.bridgeResults = {
			"ID_string" : '""', "ID_string_cont" : '""', "Ones" : '""', "Zeroes" : '""',
			"OnesZeroes" : '""', "Firmware_Ver" : '""', "Status" : '""', "TempPass" : '""',
			"HumiPass" : '""', "Scratch" : '""', "ClockCnt" : '""', "QIECount" : '""',
			"WTECount" : '""', "zeroOrbits" : '""'
		}
	

		self.iglooList = {"fpgaMajVer" : [0,0], "fpgaMinVer" : [0,0], "iglooOnes" : [0,0],
			"iglooZeros" : [0,0],"fpgaTopOrBot" : [0,0], "iglooUID" : [0,0],
			"statusReg" : [0,0], "cntrRegDisplay" : [0,0], "rst_QIE_count" : [0,0], "clk_count" : [0,0],
			"igloo_wte_count" : [0,0], "capIDErr_count" : [0,0],
			"iglooScratch" : [0,0], "Igloo2_FPGA_Control" : [0,0],
			"iglooZeros" : [0,0], "igloo_UID" : [0,0],
			"CI_Mode_On" : [0,0] , "CI_Mode_Off" : [0,0]
		}

		self.iglooResults = {
			"fpgaMajVer" : '""', "fpgaMinVer" : '""', "iglooOnes" : '""', "iglooZeros" : '""',
			"fpgaTopOrBot" : '""', "iglooUID" : '""', "statusReg" : '""', "cntrRegDisplay" : '""',
			"rst_QIE_count" : '""', "clk_count" : '""', "igloo_wte_count" : '""', "capIDErr_count" : '""',
			"iglooScratch" : '""', "Igloo2_FPGA_Control" : '""', "iglooZeros" : '""', "igloo_UID" : '""',
			"CI_Mode_On" : '""', "CI_Mode_Off" : '""'
		}

		self.longTestList = {"inputSpy_512Reads" : [0,0], "OrbitHistograms" : [0,0]}

		self.longTestResults = {"OrbitHistograms" : '""'}

		self.vttxListOne = {"vttxDisplay_1" : [0,0], "vttxRwrWithRestore_1" : [0,0]}
	
		self.vttxOneResults = {"vttxDisplay_1" : '""', "vttxRwrWithRestore_1" : '""'}

		self.vttxListTwo = {"vttxDisplay_2" : [0,0], "vttxRwrWithRestore_2" : [0,0]}

		self.vttxTwoResults = {"vttxDisplay_2" : '""', "vttxRwrWithRestore_2" : '""'}

		self.cardGenInfo["JSlot"] = self.idNo
		self.cardGenInfo["HumanLogFile"] = logFile
		self.cardGenInfo["Overwrite"] = overwrite
			
	def printResults(self):
		print ('\nGENERAL INFO: \n')
		for i in self.cardGenInfo:
			print i+ ': '+str(self.cardGenInfo[i])
		print ('BRIDGE TESTS: \n')
		for i in self.resultList:
			if (i != []):
				print i + ': '+str(self.resultList[i])
		print ('\n\nIGLOO TESTS: \n')
		for i in self.iglooList:
			print i+ ': '+str(self.iglooList[i])
		print ('\n\nVTTX_1 TESTS: \n')
		for i in self.vttxListOne:
			print i+ ': '+str(self.vttxListOne[i])
		print ('\n\nVTTX_2 TESTS: \n')
		for i in self.vttxListTwo:
			print i+ ': '+str(self.vttxListTwo[i])
		print ('\n\nLONG TESTS: \n')
		for i in self.longTestList:
			print i+ ': '+str(self.longTestList[i])


	def writeMachineJson(self):
		if (self.cardGenInfo["Unique_ID"] != ""):
			fileName = str(self.cardGenInfo["Unique_ID"].replace(" ","")+"_test_raw.json")
			with open("/home/hep/jsonResults/"+fileName, "w") as w:
				w.write("{")
				w.write('"TestType" : "Machine Readable Output"')
				for i in self.cardGenInfo.keys():
					w.write(", "+'"'+i+'"'+" : "+'"'+str(self.cardGenInfo[i])+'"')
				w.write(', "Tests" : {"TestType" : "Machine Readable Output"')
				for i in self.resultList.keys():
					w.write(", "+'"'+i+'"'+" : "+str(self.resultList[i]))
				for i in self.iglooList.keys():
					w.write(", "+'"'+i+'"'+" : "+str(self.iglooList[i]))
				for i in self.vttxListOne.keys():
					w.write(", "+'"'+i+'"'+" : "+str(self.vttxListOne[i]))
				for i in self.vttxListTwo.keys():
					w.write(", "+'"'+i+'"'+" : "+str(self.vttxListTwo[i]))
				for i in self.longTestList.keys():
					w.write(", "+'"'+i+'"'+" : "+str(self.longTestList[i]))
				w.write("\n}")
				w.write(', "ResultStrings" : {"TestType" : "Machine Readable Output"')
				for i in self.bridgeResults.keys():
					w.write(",\n "+'"'+i+'"'+" : "+self.bridgeResults[i])
				for i in self.iglooResults.keys():
					w.write(",\n "+'"'+i+'"'+" : "+self.iglooResults[i])
				for i in self.vttxOneResults.keys():
					w.write(",\n "+'"'+i+'"'+" : "+self.vttxOneResults[i])
				for i in self.vttxTwoResults.keys():
					w.write(",\n "+'"'+i+'"'+" : "+self.vttxTwoResults[i])
				for i in self.longTestResults.keys():
					w.write(",\n "+'"'+i+'"'+" : "+self.longTestResults[i])
				w.write("\n}")
				w.write("\n}")
		else:
			print 'Card has no attributes! Skipping log generation.'
