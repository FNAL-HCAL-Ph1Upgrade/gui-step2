#RM.py
from qCard import qCard
from client import *

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]

def getCardAddress(slot):
    if slot in [2,7,18,23] : return cardAddresses[0]
    if slot in [3,8,19,24] : return cardAddresses[1]
    if slot in [4,9,20,25] : return cardAddresses[2]
    if slot in [5,10,21,26]: return cardAddresses[3]


def get_NGCCM_Group(rmLoc):
    #i2cgroup dict
    return {
        1 : 0x04,
        2 : 0x02,
        3 : 0x01,
        4 : 0x20,
        5 : 0x10,
        6 : 0x20,
        7 : 0x10,
        8 : 0x02,
        9 : 0x01
                }.get([9,7,4,2][rmLoc - 1])

class RM:
    def __init__(self, location, activeSlots):
        '''Initializes an RM object at a specific location on the test stand'''
        self.qCards = []
        for i in activeSlots:
            if self.checkCards(i):
                self.qCards.append(qCard(i))
    def __repr__(self):
        '''Object representation'''
        return "RM()"
    def __str__(self):
        '''Return a string representation of RM contents'''
        s = ""
        for card in self.qCards:
            s += "qCard at %s \n" % card.slot
        return s

# This next function is a test to make sure all cards
# are actually in their slots
    def checkCards(self, slot):
    	myBus = webBus("pi5", 0)
    	activeCard = getCardAddress(slot)
    	myBus.write(activeCard,[0x00])
    	myBus.read(activeCard,4)
    	data=myBus.sendBatch()
    	if (data[0] == "1"):
    		return False
    	else:
    		return True

#    def runAll(self,barCodeList):
#        for q in range(len(self.qCards)):
#            self.qCards[q].runAll(barCodeList[q])
    def runAll(self):
    	for q in range(len(self.qCards)):
    		self.qCards[q].runAll()

    def runSingle(self, key):
    	for q in self.qCards:
    	    q.runSingle(key)
    def printAll(self):
        for q in self.qCards:
            print q
