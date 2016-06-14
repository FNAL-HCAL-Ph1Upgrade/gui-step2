#qCard class
import tests
from tests import testList

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]

def getCardAddress(slot):
    if slot in [2,7,18,23] : return cardAddresses[0]
    if slot in [3,8,19,24] : return cardAddresses[1]
    if slot in [4,9,20,25] : return cardAddresses[2]
    if slot in [5,10,21,26]: return cardAddresses[3]


class qCard:
    def __init__(self, slot, barcode='000_000'):
        '''Create a qCard object with basic info and no yet-passed tests'''
        self.slot = slot
        self.address = getCardAddress(slot)
        self.barcode = barcode
        self.passed = []
        for test in tests.testList:
            self.passed.append(0)
    def __repr__(self):
        '''Object representation'''
        return "qCard()"
    def __str__(self):
        '''Return string representation of card information'''
        s = "qCard: " + str(self.barcode) + '\n'
        for i in xrange(len(tests.testList)):
            s += "%s: %d \n" % (str(tests.testList[i]), self.passed[i])
        return s
    def runAll(self):
        '''Run all tests'''
        for i in xrange(len(tests.testList)):
            self.passed[i] = tests.testList[i](self.address)
