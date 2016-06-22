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
    ("PedastalDAC", [16,17,18,19,20,21]),
    ("CapID0pedastal", [22,23,24,25]),
    ("CapID1pedastal", [26,27,28,29]),
    ("CapID2pedastal", [30,31,32,33]),
    ("CapID3pedastal", [34, 35, 36, 37]),
    ("FixRange", [38]),
    ("RangeSet", [39, 30]),
    ("ChargeInjectDAC", [41, 42, 43]),
    ("Gsel", [44, 45, 46, 47, 48]),
    ("Idcset", [49, 50, 51, 52, 53]),
    ("CkOutEn", [54]),
    ("TDCmode", [55]),
    ("Hsel", [56]),
    ("PhaseDelay", [57, 58, 59, 60, 61, 62, 63])]
    )

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
            for i in serialShiftRegisterBits[k]:
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
            250 : (0,1),
            350 : (1,0),
            450 : (1,1)
        }.get(v, default = (-9,-9))
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
            self[5] = (0 if magnitude < 0 else 1)
            a = "%07i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(7):
                self[6 + i] = a[i]
        else:
            print "INVALID INPUT IN TimingThresholdDAC... no change made"
    #Change bits 13-15
    def TimingIref(self, q):
        d = {
            0  : (0,0,0),
            10 : (0,0,1),
            20 : (0,1,0),
            30 : (0,1,1),
            40 : (1,0,0),
            50 : (1,0,1),
            60 : (1,1,0),
            70 : (1,1,1)
        }.get(q, default=(-9,-9,-9))
        if d != (-9,-9,-9):
            self[13] = d[0]
            self[14] = d[1]
            self[15] = d[2]
        else:
            print "INVALID INPUT IN TimingIref... no change made"

    #Change bits 16-21
    def PedastalDAC(self, magnitude):
        #pedastal = magnitude * 2 fC
        #takes magnitudes -31 to 31
        if abs(magnitude) <= 31:
            self[16] = (1 if magnitude > 0 else 0)
            #set magnitude
            a = "%05i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(5):
                self[17 + i] = a[i]
        else:
            print "INVALID INPUT IN PedastalDAC... no change made"

#Change bits 22-25
    def CapID0pedastal(self, magnitude):
        #pedastal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            self[22] = (1 if magnitude > 0 else 0)
            #set magnitude
            a = "%03i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(3):
                self[23 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID0pedastal... no change made"

    #Change bits 26-29
    def CapID1pedastal(self, magnitude):
        #pedastal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            self[26] = (1 if magnitude > 0 else 0)
            #set magnitude
            a = "%03i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(3):
                self[27 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID1pedastal... no change made"

    #Change bits 30-33
    def CapID2pedastal(self, magnitude):
        #pedastal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            self[30] = (1 if magnitude > 0 else 0)
            #set magnitude
            a = "%03i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(3):
                self[31 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID2pedastal... no change made"

    #Change bits 34-37
    def CapID3pedastal(self, magnitude):
        #pedastal = magnitude * ~1.9 fC
        #takes magnitudes -12 to 12
        if abs(magnitude) <= 12:
            self[34] = (1 if magnitude > 0 else 0)
            #set magnitude
            a = "%03i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(3):
                self[35 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID3pedastal... no change made"

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
            a = "%02i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(2):
                self[39 + i] = a[i]
        else:
            print "INVALID INPUT IN RangeSet... no change made"

    #Change bits 41-43
    def ChargeInjectDAC(self, charge):
        #in fC
        d = {
            90   : (0,0,0),
            180  : (0,0,1),
            360  : (0,1,0),
            720  : (0,1,1),
            1440 : (1,0,0),
            2880 : (1,0,1),
            5760 : (1,1,0),
            8640 : (1,1,1)
        }.get(charge, default=(-9,-9,-9))
        if d != (-9,-9,-9):
            for i in xrange(3):
                self[41 + i] = d[i]
        else:
            print "INVALID INPUT IN ChargeInjectDAC... no change made"

    #Change bits 44-48
    def Gsel(self, b):
        #takes arguments 0 - 31
        if b >= 0 and b <= 31:
            a = "%05i" % int(bin(abs(magnitude))[2:])
            a = list(a)
            for i in xrange(5):
                self[44 + i] = a[i]
        else:
            print "INVALID INPUT IN Gsel... no change made"

    #Change bits 49-53
    def Idcset(self, b):
        #takes arguments 0 - 31
        if b >= 0 and b <= 31:
            a = "%05i" % int(bin(abs(magnitude))[2:])
            a = list(a)
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
            print "INVALID INPUT IN discOn... no change made"

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
            print "INVALID INPUT IN discOn... no change made"

    #Change bit 57-63
    def PhaseDelay(self, b):
        #takes arguments 0 - 127
        if b <= 127 and b >= 0:
            a = "%07i" % int(bin(abs(b))[2:])
            a = list(a)
            for i in xrange(7):
                self[57 + i] = a[i]
        else:
            print "INVALID INPUT IN CapID3pedastal... no change made"

############################################################################

############################################################################
