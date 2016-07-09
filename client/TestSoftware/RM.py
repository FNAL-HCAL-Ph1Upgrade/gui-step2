#RM.py
from qCard import qCard
import Hardware
from client import *

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]

# Given a specific card number, what hex code does it correspond to?
def getCardAddress(slot):
    if slot in [2,7,18,23] : return cardAddresses[0]
    if slot in [3,8,19,24] : return cardAddresses[1]
    if slot in [4,9,20,25] : return cardAddresses[2]
    if slot in [5,10,21,26]: return cardAddresses[3]

# Given a specific card number, what RM slot is it in?
def getReadoutSlot(slot):
    if slot in [2,3,4,5] : return     1
    if slot in [7,8,9,10] : return    2
    if slot in [18,19,20,21] : return 3
    if slot in [23,24,25,26] : return 4

# This function allows us to assign the appropriate summary
# file to a certain card, even if that card only gets used
# every now and then during testing.
def getSummaryIndex(slot):
    if slot in [2,7,18,23] : return 0
    if slot in [3,8,19,24] : return 1
    if slot in [4,9,20,25] : return 2
    if slot in [5,10,21,26]: return 3

def ngccmGroup(rm):
    i2cGroups = [0x01, 0x10, 0x20, 0x02]
    return i2cGroups[rm-1]

class RM:
    def __init__(self, location, activeSlots, summaries, inBus):
        '''Initializes an RM object at a specific location on the test stand'''
        self.qCards = []
	self.bus = inBus
	self.location = location
	emptyCount = 0
        for i in activeSlots:
	    # Only do stuff if the card is there
            if self.checkCards(i):
		print summaries[getSummaryIndex(i)].idNo   # Write the summary file's number
                self.qCards.append(qCard(i,summaries[getSummaryIndex(i)])) 

    def __repr__(self):
        '''Object representation'''
        return "RM()"
    def __str__(self):
        '''Return a string representation of RM contents'''
        s = ""
        for card in self.qCards:
            s += "qCard at %s \n" % card.slot
        return s

##Needs to be part of QIE class
##
## ^^ Doing so would create an issue
##    when assigning summary/log files
##    to each card. If we run a suite on, say, all
##    of the cards, and then we switch to run a
##    different suite on, say, half of the cards,
##    then putting this in the
##    QIE class might cause certain summary files
##    to get matched with incorrect QIE slots.
##    I.E. tests for card A would get logged in
##    the file for card B.
##    Comes into play in the for loop in __init__ - S.H.
    def checkCards(self, slot):
    	self.openChannel()
    	activeCard = getCardAddress(slot)
    	self.bus.write(0x00,[0x06])
    	self.bus.write(activeCard,[0x00])
    	self.bus.read(activeCard,4)
    	data=self.bus.sendBatch()
    	if (data[-1][0] == "1"):
    		return False
    	else:
    		return True

     # Open Channel to RM
    def openChannel(self):
     	bus = self.bus
        if self.location in [3,4]:
             # Open channel to ngCCM for RM 3,4: J1 - J10
             bus.write(0x72,[0x02])
        elif self.location in [1,2]:
             # Open channel to ngCCM for RM 1,2: J17 - J26
             bus.write(0x72,[0x01])
        else:
             print 'Invalid RM = '+str(self.location)
             print 'Please choose RM = {1,2,3,4}'
             return 'closed channel'
         # Open channel to i2c group
        bus.write(0x74, [ngccmGroup(self.location)])
       #     bus.read(0x74, 2)
        return bus.sendBatch()


    def runAll(self, suiteSelection, iters):
    	self.openChannel()
    	for q in range(len(self.qCards)):
    		self.qCards[q].runAll(self.bus, suiteSelection, iters)

    def runSingle(self, key):
	self.openChannel()
    	for q in self.qCards:
    	    q.runSingle(key,self.bus)

    def printAll(self):
        for q in self.qCards:
            print q
