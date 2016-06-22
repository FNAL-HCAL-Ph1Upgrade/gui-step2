# This is a test class that will be the bridge
# between Jordan's code and the log files.

class testSummary:
	def __init__(self):
		self.cardGenInfo = {"Barcode" : [], "Unique_ID" : [], "DateRun" : []
		}

		self.resultList = {
			"ID_string" : [], "ID_string_cont" : [], "Ones" : [],
			"Zeroes" : [], "OnesZeroes" : [], "Firmware_Ver" : [],
			"Temperature" : [], "Humidity" : [],
			"Status" : [], "TempPass" : [], "HumiPass" : [],
			"Scratch" : [], "ClockCnt" : [], "QIECount" : [],
			"WTECount" : [], "BkPln_1" : [], "BkPln_2" : [], "BkPln_3" :[],
			"OrbHist_1" : [], "OrbHist_2" : [], "OrbHist_3" : [],
			"OrbHist_4" : [], "OrbHist_5" : [] 
		}
		self.iglooList = {"fpgaMajVer" : [], "fpgaMinVer" : [], "iglooOnes" : [],
			"iglooZeros" : [],"fpgaTopOrBot" : [], "iglooUID" : [],
			"statusReg" : [], "cntrRegDisplay" : [], "rst_QIE_count" : [], "clk_count" : [],
			"igloo_wte_count" : [], "capIDErr_count" : [], "fifo_data" : [],
			"inputSpy" : [], "spy96Bits" : [], "qie_ck_ph" : [],
			"link_test_mode" : [], "link_test_pattern" : [], 
			"dataToSERDES" : [], "addrToSERDES" : [], "ctrlToSERDES" : [],
			"statFromSERDES" : [], "iglooScratch" : [], "dataFromSERDES" : [],
			"cntrRegChange" : []
		}

		self.vttxListOne = {"vttxDisplay" : [], "vttxChange" : [], "vttxRwrWithRestore" : []}
		self.vttxListTwo = {"vttxDisplay" : [], "vttxChange" : [], "vttxRwrWithRestore" : []}
			
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

	def writeHumanLog(self):
		with open("humanTest.log", "a") as w:
			w.write("\nGENERAL INFO: \n")
			for i in self.cardGenInfo:
				w.write(i+": "+str(self.cardGenInfo[i])+"\n")

			w.write("\n\nBRIDGE TESTS: \n")
			for i in self.resultList:
				w.write(i+": "+str(self.resultList[i])+"\n")
			w.write("\n")

			w.write("\n\nIGLOO TESTS: \n")
			for i in self.iglooList:
				w.write(i+": "+str(self.iglooList[i])+"\n")

			w.write("\n\n\nVTTX-1 TESTS: \n")
			for i in self.vttxListOne:
				w.write(i+": "+str(self.vttxListOne[i])+"\n")

			w.write("\n\n\nVTTX_2 TESTS: \n")
			for i in self.vttxListTwo:
				w.write(i+": "+str(self.vttxListTwo[i])+"\n")
			w.write("------------------------------------")
	
	def writeMachineJson(self):
		fileName = str(self.cardGenInfo["Unique_ID"].replace(" ","")+"_raw.json")
		with open(fileName, "w") as w:
			w.write(str(self.cardGenInfo))
			w.write("\n\n")
			w.write(str(self.resultList))
			w.write("\n\n")
			w.write(str(self.iglooList))
			w.write("\n\n")
			w.write(str(self.vttxListOne))
			w.write("\n\n")
			w.write(str(self.vttxListTwo))
