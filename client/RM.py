#RM.py
from qCard import qCard

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
        print activeSlots
        for i in activeSlots:
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
    def runAll(self):
        for q in self.qCards:
            q.runAll()
    def runSingle(key):
	q.runSingle(key)
    def printAll(self):
        for q in self.qCards:
            print q
