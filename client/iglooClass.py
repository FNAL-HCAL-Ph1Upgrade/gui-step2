from client import webBus
import QIELib
import IglooLib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib
i = IglooLib


class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logfile #changed from logstream to logfile
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
    def testBody(self):
        name = "fpgaMajVer"
        add = i.igloo[name]["address"]
        size = i.igloo[name]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, i.iglooAdd, i.igloo[name][add],i.igloo[name][size]):
            return True
        else:
            return False

def runAll():
    def openIgloo(rm,slot):
        q.openChannel(rm,slot)
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0,0)

    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["address"],'iglooClass.txt', 1)
    m.testBody()

runAll()

class fpgaMinVer(Test):
    def testBody(self):
        name = "fpgaMinVer"
        add = igloo[name]["address"]
        size = igloo[name]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[name][add],igloo[name][size]):
            return True
        else:
            return False

class ones(Test):
    def testBody():
        name = "ones"
        add = igloo[name]["address"]
        size = igloo[name]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[name][add],igloo[name][size]):
            return True
        else:
            return False

class zeroes(Test):
    def testBody():
        name = "zeroes"
        add = igloo[name]["address"]
        size = igloo[name]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[name][add],igloo[name][size]):
            return True
        else:
            return False

class fpgaTopOrBottom(Test):
    def testBody():
        name = "fpgaTopOrBottom"
        add = igloo[name]["address"]
        size = igloo[name]["size"]
        # for RO register, RWR should NOT pass
        if not readWriteRead(b, iglooAdd, igloo[name][add],igloo[name][size]):
            return True
        else:
            return False
