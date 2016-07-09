# loggerClass.py
# This file is necessary for proper writing of the human-readable
# log files. It simply changes the standard output from JUST the
# terminal to BOTH the terminal and an external file.

import sys
from time import gmtime, strftime

class logger():
	def __init__(self, fileName):
		self.name = fileName
		self.terminal = sys.stdout
		self.log = open("/home/hep/logResults/"+self.name+"_tests.log", "a")

	def write(self, message):
		ms = message.split('/n')
		t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		for m in ms:
			m = ' '.join(m.split())
			if m != '':
				o = t + "\t" + str(m) + '\n'
				self.terminal.write(o)
				self.log.write(o)

	def flush(self):
		pass

class loggerSingleTest():
	def __init__(self, fileName, testName):
		self.name = fileName
		self.testName = testName
		self.terminal = sys.__stdout__
		self.strReturn = ""
		self.log = open("/home/hep/logResults/"+self.name+"_tests.log", "a")
#		self.resultLog = open("/home/hep/logResults/"+self.name+"_"+self.testName+"_results.log", "a")

	def write(self, message):
		ms = message.split('/n')
		t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		for m in ms:
			m = ' '.join(m.split())
			if m != '':
				o = t + "\t" + str(m) + '\n'
				self.terminal.write(o)
				self.log.write(o)
				self.strReturn += (message+"\\n")
#				self.resultLog.write(o)

	def flush(self):
		pass
		
