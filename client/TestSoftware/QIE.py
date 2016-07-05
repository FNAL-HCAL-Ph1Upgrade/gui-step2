#QIE.py

#QIE settings - Ordered by most significant bits
from collections import OrderedDict
serialShiftRegisterBits = OrderedDict(
    [("LVDS/SLVS", [0]),
    ("P0, P1", [1, 2]),
    ("DiscOn", [3]),
    ("TGain", [4]),
    ("TimingThresholdDAC", [5,6,7,8,9,10,11,12]),
    ("TimingIref", [13,14,15]),
    ("PedestalDAC", [16,17,18,19,20,21]),
    ("CapID0pedestal", [22,23,24,25]),
    ("CapID1pedestal", [26,27,28,29]),
    ("CapID2pedestal", [30,31,32,33]),
    ("CapID3pedestal", [34, 35, 36, 37]),
    ("FixRange", [38]),
    ("RangeSet", [39, 40]),
    ("ChargeInjectDAC", [41, 42, 43]),
    ("Gsel", [44, 45, 46, 47, 48]),
    ("Idcset", [49, 50, 51, 52, 53]),
    ("CkOutEn", [54]),
    ("TDCmode", [55]),
    ("Hsel", [56]),
    ("PhaseDelay", [57, 58, 59, 60, 61, 62, 63])]
    )

def getBinaryList(integer, length):
    #returns a little endian
    pad = [0]*length
    a = list(bin(abs(integer))[2:])
    a.reverse()
    return a + pad[:length - len(a)]
def getBinaryListWithPolarity(integer, length):
    #returns a little endian representation with a polarity bit at the MSB
    return getBinaryList(integer, length - 1) + [1 if integer > 0 else 0]



<<<<<<< HEAD
################################################################################
# qCard Class
################################################################################
class qCard:
    def __init__(self, bus, address):
        self.address = address
        self.shiftRegisters = []
        self.readIn(bus)
    def __repr__(self):
        return "qCard()"

    def __str__(self):
        s = ""
        for i in self.shiftRegisters:
            s += str(i)
        return s
    def readIn(self, bus):
        for r in shiftRegisterAddresses:
            b = readFromRegister(bus, self.address, r, 48)
            self.shiftRegisters.append(QIEshiftRegister(getBitsFromBytes(b)))
    def writeOut(self, bus):
        for i in range(2):
            writeToRegister(bus, self.address, shiftRegisterAddresses[i],\
            getBytesFromBits(self.shiftRegisters[i].flatten()))
################################################################################

def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[1].split():
        ret.append(int(i))
    return ret
def writeToRegister(bus, address, register, bytesToWrite):
    bus.write(address, [register] + list(bytesToWrite))
    return None

################################################################################
# BridgeRegister Class
################################################################################
class bridgeRegisters:
    def __init__(self, name, correctVal, address, bits, write):
        self.name = name
        self.correctVal = correctVal
        self.address = address
        self.bits = bits
        self.write = write

################################################################################
# QIEshiftRegister Class
################################################################################
class QIEshiftRegister:
    def __init__(self, arr = list(0 for i in xrange(64 * 6))):
        '''creates a shift register object with 6 QIEs, default 0s'''
        self.QIEs = []
        for i in xrange(6):
            self.QIEs.append(QIE(arr[i * 64:(i + 1) * 64]))


    def __repr__(self):
        return "shiftRegister()"

    def __str__(self):
        r = ""
        for q in self.QIEs:
            r += "-------\n"
            r += str(q)
            r += "\n"
            r += "-------\n"
        return r
    #returns a flattened array of all QIE register bits to be written as a block
    def flatten(self):
        '''flatten all of the bits in the register's QIEs to one list'''
        a = []
        for q in self.QIEs:
            a += q.flatten()
        return a
################################################################################


################################################################################
# QIE Class
################################################################################
=======
=======
>>>>>>> 2c9cb6e81a2318840860f4a8699d67561597f442

#QIE Class
class QIE:
    ############################################################################
    # Core and I/O Functions
    ############################################################################
    def __init__(self, arrayOfBits = list(0 for i in xrange(64))):
        '''initialize a QIE11 object with given bits set'''
        self.load(arrayOfBits)
    def __repr__(self):
        return "QIE()"
    def __str__(self):
        '''Display each setting with values'''
        strs = []
        for k in serialShiftRegisterBits.keys():
            s = ""
            b = list(serialShiftRegisterBits[k])
            b.reverse()
            for i in b:
                s += str(self.arr[i])
            strs.append(k + ":\n    " + s)
        return "\n".join(strs)
    def __getitem__(self, i):
        return self.arr[i]
    def __setitem__(self, i, item):
        self.arr[i] = item
    def flatten(self):
        return list(int(i) for i in self)
    def load(self, arrayOfBits):
        self.arr = arrayOfBits
    ############################################################################


    ############################################################################
    #Functions to change bits by property
    ############################################################################
    #Change bit 0
    def setLVDS(self):
        self[0] = 1
    def setSLVS(self):
        self[0] = 0

    #Change bits 1-2
    def setLVDS_output_level_trim(self, v):
        d = {
            150 : (0,0),
            250 : (1,0),
            350 : (0,1),
            450 : (1,1)
        }.get(v, (-9,-9))
        if d == (-9, -9):
            print "INVALID INPUT IN setLVDS_output_level_trim... no change made"
        else:
            self[1] = d[0]
            self[2] = d[1]

    #Change bit 3
    def discOn(self, b):
        if b == 0:
            self[3] = 0
        elif b == 1:
            self[3] = 1
        else:
            print "INVALID INPUT IN discOn... no change made"

    #Change bit 4
    def TGain(self, b):
        if b == 0:
            self[4] = 0
        elif b == 1:
            self[4] = 1
        else:
            print "INVALID INPUT IN TGain... no change made"

    #Change bits 5-12
    def TimingThresholdDAC(self, magnitude):
        #accepts magnitudes -127 to 127
        if abs(magnitude) <= 127:
            a = getBinaryListWithPolarity(magnitude, 8)
            for i in xrange(8):
                self[5 + i] = a[i]
        else:
            print "INVALID INPUT IN TimingThresholdDAC... no change made"
    #Change bits 13-15
    def TimingIref(self, q):
        d = {
            0  : (0,0,0),
            10 : (1,0,0),
            20 : (0,1,0),
            30 : (1,1,0),
            40 : (0,0,1),
            50 : (1,0,1),
            60 : (0,1,1),
            70 : (1,1,1)
        }.get(q, (-9,-9,-9))
        if d != (-9,-9,-9):
            self[13] = d[0]
            self[14] = d[1]
            self[15] = d[2]
        else:
            print "INVALID INPUT IN TimingIref... no change made"

    #Change bits 16-21
    def PedestalDAC(self, magnitude):
        #pedestal = magnitude * 2 fC
        #takes magnitudes -31 to 31
        if abs(magnitude) <= 31:
            a = getBinaryListWithPolarity(magnitude, 6)
            for i in xrange(6):
                self[16 + i] = a[i]
        else:
            print "INVALID INPUT IN PedestalDAC... no change made"

#Change bits 22-25
    def CapID0pedestal(self, magnitude):
        #pedestal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            a = getBinaryListWithPolarity(magnitude, 4)
            for i in xrange(4):
                self[22 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID0pedestal... no change made"

    #Change bits 26-29
    def CapID1pedestal(self, magnitude):
        #pedestal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            a = getBinaryListWithPolarity(magnitude, 4)
            for i in xrange(4):
                self[26 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID1pedestal... no change made"

    #Change bits 30-33
    def CapID2pedestal(self, magnitude):
        #pedestal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            a = getBinaryListWithPolarity(magnitude, 4)
            for i in xrange(4):
                self[30 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID2pedestal... no change made"

    #Change bits 34-37
    def CapID3pedestal(self, magnitude):
        #pedestal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            a = getBinaryListWithPolarity(magnitude, 4)
            for i in xrange(4):
                self[34 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID3pedestal... no change made"

    #Change bits 38
    def FixRange(self, b):
        if b == 1 or b == 0:
            #fixed range mode = 1, autorange mode = 0
            self[38] = b
        else:
            print "INVALID INPUT IN FixRange... no change made"

    #Change bits 39-40
    def RangeSet(self, b):
        #takes 0, 1, 2, or 3
        if b >= 0 and b <= 3:
            a = getBinaryList(b, 2)
            for i in xrange(2):
                self[39 + i] = a[i]
        else:
            print "INVALID INPUT IN RangeSet... no change made"

    #Change bits 41-43
    def ChargeInjectDAC(self, charge):
        #in fC
        d = {
            90   : (0,0,0),
            180  : (1,0,0),
            360  : (0,1,0),
            720  : (1,1,0),
            1440 : (0,0,1),
            2880 : (1,0,1),
            5760 : (0,1,1),
            8640 : (1,1,1)
        }.get(charge, (-9,-9,-9))
        if d != (-9,-9,-9):
            for i in xrange(3):
                self[41 + i] = d[i]
        else:
            print "INVALID INPUT IN ChargeInjectDAC... no change made"

    #Change bits 44-48
    def Gsel(self, b):
        #takes arguments 0 - 31
        if b >= 0 and b <= 31:
            a = getBinaryList(b, 5)
            for i in xrange(5):
                self[44 + i] = a[i]
        else:
            print "INVALID INPUT IN Gsel... no change made"

    #Change bits 49-53
    def Idcset(self, b):
        #takes arguments 0 - 31
        if b >= 0 and b <= 31:
            a = getBinaryList(b, 5)
            for i in xrange(5):
                self[49 + i] = a[i]
        else:
            print "INVALID INPUT IN Idcset... no change made"
    #Change bit 54
    def CkOutEn(self, b):
        if b == 0:
            self[54] = 0
        elif b == 1:
            self[54] = 1
        else:
            print "INVALID INPUT IN CkOutEn... no change made"

    #Change bit 55
    def TDCmode(self, b):
        if b == 0:
            self[55] = 0
        elif b == 1:
            self[55] = 1
        else:
            print "INVALID INPUT IN TDCmode... no change made"

    #Change bit 56
    def Hsel(self, b):
        if b == 0:
            #hysteresis is less than p2p noise
            self[56] = 0
        if b == 1:
            #amount of hysteresis is doubled as compared to b = 0
            self[56] = 1
        else:
            print "INVALID INPUT IN Hsel... no change made"

    #Change bit 57-63
    def PhaseDelay(self, b):
        #takes arguments 0 - 127
        if b <= 127 and b >= 0:
            a = getBinaryList(b, 7)
            for i in xrange(7):
                self[57 + i] = a[i]
        else:
            print "INVALID INPUT IN PhaseDelay... no change made"


##############################################

    #Change bits 41-43
    def getChargeInjectDAC(self):
        #in fC
        d = {
            90   : (0,0,0),
            180  : (1,0,0),
            360  : (0,1,0),
            720  : (1,1,0),
            1440 : (0,0,1),
            2880 : (1,0,1),
            5760 : (0,1,1),
            8640 : (1,1,1)
        }.get(charge, (-9,-9,-9))
        if d != (-9,-9,-9):
            for i in xrange(3):
                self[41 + i] = d[i]
        else:
            print "INVALID INPUT IN ChargeInjectDAC... no change made"


############################################################################

############################################################################
