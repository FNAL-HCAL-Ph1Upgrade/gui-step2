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
    def flatten(self):
        return list(self.arr)
    def load(self, arrayOfBits):
        self.arr = arrayOfBits
    ############################################################################


    ############################################################################
    #Functions to change bits by property
    ############################################################################
    #Change bit 0
    def setLVDS(self):
        self.arr[0] = 1
    def setSLVS(self):
        self.arr[0] = 0

    #Change bits 1-2
    def setLVDS_output_level_trim(self, v):
        d = {
            150 : (0,0),
            250 : (0,1),
            350 : (1,0),
            450 : (1,1)
        }.get(v)
        self.arr[1] = d[0]
        self.arr[2] = d[1]

    #Change bit 3
    def discOn(self, b):
        if b == 0:
            self.arr[3] = 0
        elif b == 1:
            self.arr[3] = 1

    #Change bit 4
    def TGain(self, b):
        if b == 0:
            self.arr[4] = 0
        elif b == 1:
            self.arr[4] = 1

    #Change bits 5-12
    def TimingThresholdDAC(self, t):
        for i in xrange(8):
            self.arr[i + 5] = t[i]

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
        }.get(q)
        self.arr[13] = d[0]
        self.arr[14] = d[1]
        self.arr[15] = d[2]

    #Change bits 16-21
    def PedastalDAC(self, polarity, magnitude):
        #pedastal = polarity * magnitude * 2 fC
        if polarity == 1:
            self.arr[16] = 1
        elif polarity == 0 or polarity == -1:
            self.arr[16] = 0
        #set magnitude
        bits = getBits(magnitude)
        for i in xrange(5):
            self.arr[17 + i] = bits[i]

#Change bits 22-25
    def CapID0pedastal(self, polarity, magnitude):
        #pedastal = polarity * magnitude * ~1.9 fC
        if polarity == 1:
            self.arr[22] = 1
        elif polarity == 0 or polarity == -1:
            self.arr[22] = 0
        #set magnitude
        bits = getBits(magnitude)
        for i in xrange(3):
            self.arr[23 + i] = bits[i]

    #Change bits 26-29
    def CapID1pedastal(self, polarity, magnitude):
        #pedastal = polarity * magnitude * ~1.9 fC
        if polarity == 1:
            self.arr[26] = 1
        elif polarity == 0 or polarity == -1:
            self.arr[26] = 0
        #set magnitude
        bits = getBits(magnitude)
        for i in xrange(3):
            self.arr[27 + i] = bits[i]

    #Change bits 30-33
    def CapID2pedastal(self, polarity, magnitude):
        #pedastal = polarity * magnitude * ~1.9 fC
        if polarity == 1:
            self.arr[30] = 1
        elif polarity == 0 or polarity == -1:
            self.arr[30] = 0
        #set magnitude
        bits = getBits(magnitude)
        for i in xrange(3):
            self.arr[31 + i] = bits[i]

    #Change bits 34-37
    def CapID3pedastal(self, polarity, magnitude):
        #pedastal = polarity * magnitude * ~1.9 fC
        if polarity == 1:
            self.arr[34] = 1
        elif polarity == 0 or polarity == -1:
            self.arr[34] = 0
        #set magnitude
        bits = getBits(magnitude)
        for i in xrange(3):
            self.arr[35 + i] = bits[i]

    #Change bits 38
    def FixRange(self, b):
        if b == 1:
            #fixed range mode
            self.arr[38] = 1
        elif b == 0:
            #autorange mode
            self.arr[38] = 0

    #Change bits 39-40
    def RangeSet(self, t):
        self.arr[39] = t[0]
        self.arr[40] = t[1]

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
        }.get(charge)
        for i in xrange(3):
            self.arr[41 + i] = d[i]

    #Change bits 44-48
    def Gsel(self, t):
        for i in xrange(5):
            self.arr[44 + i] = t[i]

    #Change bits 49-53
    def Idcset(self, t):
        for i in range(5):
            self.arr[49 + i] = t[i]

    #Change bit 54
    def CkOutEn(self, b):
        if b == 0:
            #Disable LVDS CkOut
            self.arr[54] = 0
        elif b == 1:
            #Enable LVDS CkOut
            self.arr[54] = 1

    #Change bit 55
    def TDCmode(self, b):
        if b == 0:
            #First mode
            self.arr[55] = 1
        elif b == 1:
            #Last mode
            self.arr[55] = 1

    #Change bit 56
    def Hsel(self, b):
        if b == 0:
            #hysteresis is less than p2p noise
            self.arr[56] = 0
        if b == 1:
            #amount of hysteresis is doubled as compared to b = 0
            self.arr[56] = 1

    #Change bit 57-63
    def PhaseDelay(self, t):
        for i in xrange(7):
            self.arr[57 + i] = t[i]

############################################################################

############################################################################
