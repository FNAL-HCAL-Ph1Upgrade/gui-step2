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
		
