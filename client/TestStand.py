#TestStand.py

import RM

class TestStand:
    def __init__(self, activeSlots):
        '''Create a test stand object filled with necessary RMs, cards'''

        self.activeSlots = activeSlots
        self.RMs = []

        RM4_active = []
        RM3_active = []
        RM2_active = []
        RM1_active = []

        for slot in self.activeSlots:
            if slot in [2,3,4,5]:
                #RM4
                RM4_active.append(slot)
            elif slot in [7,8,9,10]:
                #RM3
                RM3_active.append(slot)
            elif slot in [18,19,20,21]:
                #RM2
                RM2_active.append(slot)
            elif slot in [23,24,25,26]:
                #RM1
                RM1_active.append(slot)
        #initialize RMs
        self.RMs.append(RM.RM(1, RM1_active))
        self.RMs.append(RM.RM(2, RM2_active))
        self.RMs.append(RM.RM(3, RM3_active))
        self.RMs.append(RM.RM(4, RM4_active))

    def runAll(self,barCodeList):
	for r in self.RMs:
		r.runAll(barCodeList)

    def runSingle(self, key):
	for r in self.RMs:
		r.runSingle(key)

    def __repr__(self):
        '''Object representation'''
        return "TestStand()"
    def __str__(self):
        '''Return string representation of object data'''
        s = ""
        for i in xrange(len(self.RMs)):
            s += "RM%i:\n%s\n" % (i, str(self.RMs[i]))
        return s
