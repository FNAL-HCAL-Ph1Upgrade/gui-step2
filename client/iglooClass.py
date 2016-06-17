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
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody() == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
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
        # if not (i.RWR_noChange(b, i.iglooAdd, reg, size)):
        #     return True
        # else:
        #     return False

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
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
        # if not (i.RWR_noChange(b, i.iglooAdd, reg, size)):
        #     return True
        # else:
        #     return False

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ones(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ones"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------
class zeroes(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "zeroes"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaTopOrBottom(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaTopOrBottom"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------
class uniqueID(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "uniqueID"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, RWR should NOT pass
        if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
            return True
        else:
            return False
# ------------------------------------------------------------------------

class statusReg(Test): #inherit from Test class, overload testBody() function
    def read(self, desiredReg = "all"):
        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister(b, i.iglooAdd, reg, size)
        print "allRegList: ", allRegList

        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        statusReg = {
            "InputSpyWordNum"   :   allRegStr[0:10], # number of words in InputSpyFifo (depth = 512)
            "InputSpyFifoEmpty" :   allRegStr[10],
            "InputSpyFifoFull"  :   allRegStr[11],
            "Qie_DLLNoLock"     :   allRegStr[12:24], # good when '0'
            "BRIDGE_SPARE"      :   allRegStr[24:30],
            "1_bit"             :   allRegStr[30], # should be '0'
            "PLL_320MHz_Lock"   :   allRegStr[31] # good when '1'
            }

        allReg = statusReg["InputSpyWordNum"] + " : " + statusReg["InputSpyFifoEmpty"]\
            + " : " + statusReg["InputSpyFifoFull"] + " : " + statusReg["Qie_DLLNoLock"]\
            + " : " + statusReg["BRIDGE_SPARE"] + " : " + statusReg["1_bit"]\
            + " : " + statusReg["PLL_320MHz_Lock"]

        if desiredReg == "all":
            return allReg
            
        else:
            return statusReg[desiredReg]

    def write(self, name, settingBits):
        # CODE HERE
        return True

    def testBody(self):
        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        print self.read(self)
        # # for RO register, RWR should NOT pass
        # if (i.RWR_randChange(b, i.iglooAdd, reg, size)):
        #     return True
        # else:
        #     return False
# ------------------------------------------------------------------------
def runAll():
    def openIgloo(rm,slot):
        q.openChannel(rm,slot)
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0,0)

    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaMinVer(b,i.igloo["fpgaMinVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = ones(b,i.igloo["ones"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = zeroes(b,i.igloo["zeroes"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaTopOrBottom(b,i.igloo["fpgaTopOrBottom"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = uniqueID(b,i.igloo["uniqueID"]["register"],'iglooClass.txt', 2)
    print m.run()
    m = statusReg(b,i.igloo["statusReg"]["register"],'iglooClass.txt', 2)
    print m.run()

runAll()
