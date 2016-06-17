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

# ------------------------------------------------------------------------

class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMajVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        # print "----------NO CHANGE----------"
        # # for RO register, RWR should NOT pass
        # if not (i.readWriteRead_noChange(b, i.iglooAdd, reg, size)):
        #     return True
        # else:
        #     return False

        print "----------RAND CHANGE----------"
        # for RO register, RWR should NOT pass
        if (i.readWriteRead_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------

class fpgaMinVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMinVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        # print "----------NO CHANGE----------"
        # # for RO register, RWR should NOT pass
        # if not (i.readWriteRead_noChange(b, i.iglooAdd, reg, size)):
        #     return True
        # else:
        #     return False

        print "----------RAND CHANGE----------"
        # for RO register, RWR should NOT pass
        if (i.readWriteRead_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------

def runAll():
    def openIgloo(rm,slot):
        q.openChannel(rm,slot)
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0,1)

    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["register"],'iglooClass.txt', 4)
    print m.testBody()
    m = fpgaMinVer(b,i.igloo["fpgaMinVer"]["register"],'iglooClass.txt', 4)
    print m.testBody()

runAll()
