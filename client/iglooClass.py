from client import webBus
import QIELib
import IglooLib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib


class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logstream
        self.iterations = iterations
    def run(self):
        passes = 0
        for i in xrange(iterations):
            if self.testBody() == true: passes += 1
        return (passes, fails)
    def log(self, message):
        logprint(message, file=self.logfile)
    def testBody(self):
        return True

class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody():
        reg = "fpgaMajVer"
        add = igloo[reg]["address"]
        size = igloo[reg]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[reg][add],igloo[reg][size]):
            return True
        else:
            return False

fpgaMajVer(b,igloo["fpgaMajVer"]["address"],iglooClass.txt, 1)

class fpgaMinVer(Test):
    def testBody():
        reg = "fpgaMinVer"
        add = igloo[reg]["address"]
        size = igloo[reg]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[reg][add],igloo[reg][size]):
            return True
        else:
            return False

class ones(Test):
    def testBody():
        reg = "ones"
        add = igloo[reg]["address"]
        size = igloo[reg]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[reg][add],igloo[reg][size]):
            return True
        else:
            return False

class zeroes(Test):
    def testBody():
        reg = "zeroes"
        add = igloo[reg]["address"]
        size = igloo[reg]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[reg][add],igloo[reg][size]):
            return True
        else:
            return False

class fpgaTopOrBottom(Test):
    def testBody():
        reg = "fpgaTopOrBottom"
        add = igloo[reg]["address"]
        size = igloo[reg]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[reg][add],igloo[reg][size]):
            return True
        else:
            return False
