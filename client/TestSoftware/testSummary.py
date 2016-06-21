# This is a test class that will be the bridge
# between Jordan's code and the log files.

class testSummary:
	def __init__(self):
		self.resultList = {
			"ID_string" : [], "ID_string_cont" : [], "Ones" : [],
			"Zeroes" : [], "OnesZeroes" : [], "Firmware_Ver" : [],
			"Unique_ID" : [], "Temperature" : [], "Humidity" : [],
			"Barcode" : [], "Status" : [], "TempPass" : [], "HumiPass" : [],
			"Scratch" : [], "ClockCnt" : [], "QIECount" : [],
			"WTECount" : [], "BkPln_1" : [], "BkPln_2" : [], "BkPln_3" :[],
			"OrbHist_1" : [], "OrbHist_2" : [], "OrbHist_3" : [],
			"OrbHist_4" : [], "OrbHist_5" : [] 
		}
		self.iglooList = {"fpgaMajVer" : [], "fpgaMinVer" : [], "iglooOnes" : [],
			"iglooZeros" : [],"fpgaTopOrBot" : [], "iglooUID" : [],
			"statusReg" : [], "cntrRegDispaly" : [], "cntrRegChange" : [],
			"cntrRegTerminalChange" : [], "rst_QIE_count" : [], "clk_count" : [],
			"igloo_wte_count" : [], "capIDErr_count" : [], "fifo_data" : [],
			"inputSpy" : [], "spy96Bits" : [], "qie_ck_ph" : [],
			"link_test_mode" : [], "link_test_pattern" : [], 
			"dataToSERDES" : [], "addrToSERDES" : [], "ctrlToSERDES" : [],
			"statFromSERDES" : [], "iglooScratch" : []
		}
			
	def printResults(self):
		for i in self.resultList:
			if (i != []):
				print i + ": ", self.resultList[i]

	def writeHumanLog(self):
		with open("humanTest.log", "a") as w:
			for i in self.resultList:
				w.write(i+": "+str(self.resultList[i])+"\n")
			w.write("\n")
	
	def writeMachineJson(self):
		fileName = str(self.resultList["Unique_ID"][0].replace(" ","")+"_raw.json")
		with open(fileName, "w") as w:
			w.write(str(self.resultList))
