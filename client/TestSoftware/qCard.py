#qCard class
import testSummary
import tests
import Hardware

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]

def getCardAddress(slot):
	if slot in [2,7,18,23] : return cardAddresses[0]
	if slot in [3,8,19,24] : return cardAddresses[1]
	if slot in [4,9,20,25] : return cardAddresses[2]
	if slot in [5,10,21,26]: return cardAddresses[3]

class qCard:
    def __init__(self, slot, summary, barcode='000_000'):
        '''Create a qCard object with basic info and no yet-passed tests'''
        self.slot = slot
        self.address = getCardAddress(self.slot)
        self.barcode = barcode
        self.passed = []
	self.outCard = summary

    def __repr__(self):
        '''Object representation'''
        return "qCard()"
    def __str__(self):
        '''Return string representation of card information'''
        s = "qCard: %s at slot %s\n" % (self.barcode, self.slot)
        for i in xrange(len(self.passed)):
            s += "Test%s: %s \n" % (i, str(self.passed[i]))
        return s

#   def runAll(self,barcode):
    def runAll(self, inBus, suiteSelection, iters):
        '''Run all tests'''
        t = tests.testSuite(inBus, self.address, self.outCard, iters)
	t.runTests(suiteSelection)

    def runSingle(self, key,piAddress):
	    t = tests.testSuite(piAddress, self.address)
	    for result in t.runSingleTest(key):
    	        self.passed.append(result)
	    print self.passed
