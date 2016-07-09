from client import webBus
from Test import Test
import vttxLib

v = vttxLib

# ------------------------------------------------------------------------
class VTTX_Display(Test):
    def testBody(self):
#        print '----------VTTX_Display----------'
        read1 = v.readFromVTTX(self.bus, v.vttx["address"], v.vttx['size'])

        if read1 == False: return False
        else:
#            print '~~ PASS: VTTX Register: '+str(read1)
            return True
# ------------------------------------------------------------------------
class VTTX_Change(Test): # NOTE: the run() function is overloaded & takes list parameter toWrite
    def testBody(self, toWrite):
#        print '----------VTTX_Change----------'
        w = v.writeToVTTX(self.bus, v.vttx['address'], v.vttx['size'], toWrite)

        if w == False: return False
        else:
#            print '~~ PASS: VTTX Register: '+str(read1)
            return True

    def run(self, toWrite):
        passes = 0
        for i in xrange(self.iterations):
            if self.testBody(toWrite) == True: passes += 1
        return (passes, self.iterations - passes)

class VTTX_RWR_withRestore(Test):
    def testBody(self):
#        print '----------VTTX_RWR_withRestore----------'
        ret = v.RWR_withRestore(self.bus, v.vttx['address'], v.vttx['size'])
        if ret == True:
#            print '~~ PASS: RWR Success ~~'
            return True
        else:
            return False

