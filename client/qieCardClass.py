# qieCardClass.py
#
# This is a class that will contain basic information
# about an individual QIE Card along with how it fared
# on the tests that it was subjected to.
#
# Created on June 10 2016

class qieCard:
	def __init__(self):
		# Create variables to store information 
	
		# Test parameters/info
		self.timeOfTest = ""
		self.tester     = ""
		
		# Data from card
		self.i2cAddress  = ""
		self.uniqueID    = ""
		self.temperature = -999.99
		self.humidity    = -999.99
		self.firmwareVer = ""

		# Test results
		self.passedTemp  = False
		self.passedHumid = False
		self.passedHerm  = False
		self.passedBrdg  = False
		self.passedOnes  = False
		self.passedZero  = False
