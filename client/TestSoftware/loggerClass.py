# loggerClass.py
# This file is necessary for proper writing of the human-readable
# log files. It simply changes the standard output from JUST the
# terminal to BOTH the terminal and an external file.

import sys

class logger():

	def __init__(self, fileName):
		self.terminal = sys.stdout
		self.log = open(fileName, "a")

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)

	def flush(self):
		pass
		
