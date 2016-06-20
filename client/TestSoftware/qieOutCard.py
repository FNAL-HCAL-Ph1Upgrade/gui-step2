# This is a test class that will be the bridge
# between Jordan's code and the log files.

class qCardOut:
	def __init__(self):
		self.resultList = {
			"ID_string" : [], "ID_string_cont" : [], "Ones" : [],
			"Zeroes" : [], "OnesZeroes" : [], "Firmware_Ver" : [],
			"Unique_ID" : [], "Temperature" : [], "Humidity" : []
		}
			
	def printResults(self):
		for i in self.resultList:
			print i + ": ", self.resultList[i]

	def writeHumanLog(self):
		with open("testHuman.log", "a") as w:
			for i in self.resultList:
				w.write(i+": "+str(self.resultList[i])+"\n")
			w.write("\n")
