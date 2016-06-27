#DaisyChain.py
#QIE DaisyChain class

from QIE import QIE


class DaisyChain:
    def __init__(self, arr = list(0 for i in xrange(64 * 6))):
        '''creates a shift register object with 6 QIEs, default 0s'''
        self.QIEs = []
        for i in xrange(6):
            self.QIEs.append(QIE(arr[i * 64:(i + 1) * 64]))
        #Adry (6/24)
        # for i in xrange(6):
        #     self.CI.append(QIE(arr[]))
    def __repr__(self):
        return "DaisyChain()"
    def __str__(self):
        r = ""
        for q in self.QIEs:
            r += "-------\n"
            r += str(q)
            r += "\n"
            r += "-------\n"
        return r
    def __getitem__(self, i):
        return self.QIEs[i]
    #returns a flattened array of all QIE register bits to be written as a block
    def flatten(self):
        '''flatten all of the bits in the register's QIEs to one list'''
        a = []
        for q in self.QIEs:
            a += q.flatten()
        return a
    # def getCI(self):

################################################################################
