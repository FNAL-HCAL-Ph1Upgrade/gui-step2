# loggerClass.py
# This file is necessary for proper writing of the human-readable
# log files. It simply changes the standard output from JUST the
# terminal to BOTH the terminal and an external file.

import sys
from time import gmtime, strftime

class logger():

	def __init__(self, fileName):
		self.terminal = sys.stdout
		self.log = open("/home/hep/logResults/"+fileName, "a")

	def write(self, message):
		ms = message.split('/n')
		t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		for m in ms:
			o = t + "\t" + str(message)
			self.terminal.write(o)
			self.log.write(o)
			
	def flush(self):
		pass
