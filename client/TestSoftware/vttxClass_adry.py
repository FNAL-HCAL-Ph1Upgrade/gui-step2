from client import webBus
import vttxLib
import TestSoftware.Hardware as Hardware

h = Hardware

b = webBus('pi5',0) #can add 'pi5,0' so won't print send/receive messages
v = vttxLib

slot = 18 # the J_# slot

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
class VTTX_Display(Test):
    def testBody(self):
        print '----------VTTX_Display----------'
        read1 = v.readFromVTTX(b, v.vttx["address"], v.vttx['size'])

        if read1 == False: return False
        else:
            print '~~ PASS: VTTX Register: '+str(read1)
            return True
# ------------------------------------------------------------------------
class VTTX_Change(Test): # NOTE: the run() function is overloaded & takes list parameter toWrite
    def testBody(self, toWrite):
        print '----------VTTX_Change----------'
        w = v.writeToVTTX(b, v.vttx['address'], v.vttx['size'], toWrite)

        if w == False: return False
        else:
            print '~~ PASS: VTTX Register: '+str(read1)
            return True

    def run(self, toWrite):
        passes = 0
        for i in xrange(self.iterations):
            if self.testBody(toWrite) == True: passes += 1
        return (passes, self.iterations - passes)

class VTTX_RWR_withRestore(Test):
    def testBody(self):
        print '----------VTTX_RWR_withRestore----------'
        ret = v.RWR_withRestore(b, v.vttx['address'], v.vttx['size'])
        if ret == True:
            print '~~ PASS: RWR Success ~~'
            return True
        else:
            return False

# ---------RUN FUNCTIONS--------------------------------------------------
def runAll():
    # -------VTTX 1----------
    print '----------------------VTTX 1-------------------------'
    v.openVTTX(slot,1) #USE openVTTX 2nd parameter to select VTTX NUMBER!

    m = VTTX_Display(b, v.vttx['address'], 'vttx.txt', 2)
    print m.run()
    # m = VTTX_Change(b, vttx['address'], 'vttx.txt', 1)
    # print m.run() #TO ACTUALLY USE -> PARAMETER = toWrite list of 7 bytes

    m = VTTX_RWR_withRestore(b, v.vttx['address'], 'vttx.txt', 2)
    print m.run()

    # -------VTTX 2----------
    #print '\n'
    print '----------------------VTTX 2-------------------------'
    v.openVTTX(slot,2) #USE openVTTX 2nd parameter to select VTTX NUMBER!

    m = VTTX_Display(b, v.vttx['address'], 'vttx.txt', 2)
    print m.run()
    # m = VTTX_Change(b, vttx['address'], 'vttx.txt', 1)
    # print m.run() #TO ACTUALLY USE -> PARAMETER = toWrite list of 7 bytes

    m = VTTX_RWR_withRestore(b, v.vttx['address'], 'vttx.txt', 2)
    print m.run()

    #print '\n\n'
runAll()
