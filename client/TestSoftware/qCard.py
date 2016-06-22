#qCard class
import tests
from Hardware import Hardware

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]

class qCard:
    def __init__(self, slot, bus, barcode='000_000'):
        '''Create a qCard object with basic info and no yet-passed tests'''
        self.slot = slot
        self.address = Hardware.getCardAddress(slot)
        self.barcode = barcode
        self.passed = []
    def __repr__(self):
        '''Object representation'''
        return "qCard()"
    def __str__(self):
        '''Return string representation of card information'''
        s = "qCard: %s at slot %s\n" % (self.barcode, self.slot)
        for i in xrange(len(self.passed)):
            s += "Test%s: %s \n" % (i, str(self.passed[i]))
        return s
#    def runAll(self,barcode):
    def runAll(self,piAddress):
        '''Run all tests'''
        Hardware.openChannel(self.slot)
        t = tests.testSuite(piAddress, self.address)
#	t.runTests(barcode)
	t.runTests()

    def runSingle(self, key,piAddress):
        Hardware.openChannel(self.slot)
	    t = tests.testSuite(piAddress, self.address)
	    for result in t.runSingleTest(key):
            self.passed.append(result)
	    print self.passed
