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
		self.iglooList = {"fpgaMajVer" : [0,0], "fpgaMinVer" : [0,0], "iglooOnes" : [0,0],
			"iglooZeros" : [0,0],"fpgaTopOrBot" : [0,0], "iglooUID" : [0,0],
			"statusReg" : [0,0], "cntrRegDisplay" : [0,0], "rst_QIE_count" : [0,0], "clk_count" : [0,0],
			"igloo_wte_count" : [0,0], "capIDErr_count" : [0,0], "fifo_data" : [0,0],
			"spy96Bits" : [0,0], "qie_ck_ph" : [0,0],
			"link_test_mode" : [0,0], "link_test_pattern" : [0,0], 
			"dataToSERDES" : [0,0], "addrToSERDES" : [0,0], "ctrlToSERDES" : [0,0],
			"statFromSERDES" : [0,0], "iglooScratch" : [0,0], "dataFromSERDES" : [0,0],
			"iglooZeros" : [0,0], "igloo_UID" : [0,0], "Igloo2_FPGA_Control" : [0,0],
			"CI_Mode_On" : [0,0] , "CI_Mode_Off" : [0,0]
		}

		self.longTestList = {"inputSpy_512Reads" : [0,0], "OrbitHistograms" : [0,0]}

		self.vttxListOne = {"vttxDisplay_1" : [0,0], "vttxChange_1" : [0,0], "vttxRwrWithRestore_1" : [0,0]}
		self.vttxListTwo = {"vttxDisplay_2" : [0,0], "vttxChange_2" : [0,0], "vttxRwrWithRestore_2" : [0,0]}

		self.cardGenInfo["JSlot"] = self.idNo
		self.cardGenInfo["HumanLogFile"] = logFile
		self.cardGenInfo["Overwrite"] = overwrite
			
	def printResults(self):
		print ("\nGENERAL INFO: \n")
		for i in self.cardGenInfo:
			print i+ ": ", self.cardGenInfo[i]
		print ("BRIDGE TESTS: \n")
		for i in self.resultList:
			if (i != []):
				print i + ": ", self.resultList[i]
		print ("\n\nIGLOO TESTS: \n")
		for i in self.iglooList:
			print i+ ": ", self.iglooList[i]
		print ("\n\nVTTX_1 TESTS: \n")
		for i in self.vttxListOne:
			print i+ ": ", self.vttxListOne[i]
		print ("\n\nVTTX_2 TESTS: \n")
		for i in self.vttxListTwo:
			print i+ ": ", self.vttxListTwo[i]
		print ("\n\nLONG TESTS: \n")
		for i in self.longTestList:
			print i+ ": ", self.longTestList[i]


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
				w.write("\n}")
				w.write("\n}")
		else:
			print "Card has no attributes! Skipping log generation."
