#!/usr/bin/python
#
#QIELib.py
#Library of tables, functions, and classes for working with QIE11 test stands


shiftRegisterAddresses = [0x30, 0x31]

#Bit to write to mux for given twisted pair i2c
i2cGroups = {
    1 : 0x04,
    2 : 0x02,
    3 : 0x01,
    4 : 0x20,
    5 : 0x10,
    6 : 0x20,
    7 : 0x10,
    8 : 0x02,
    9 : 0x01
            }
RMs = {
    4 : {
        "slots" : [2,3,4,5],
        "sipm" : 1,
        "slotGroup" : 2,
        "sipmGroup" : 1
        },
    3 : {
        "slots" : [7,8,9,10],
        "sipm" : 6,
        "slotGroup" : 4,
        "sipmGroup" : 3
        },
    2 : {
        "slots" : [18,19,20,21],
        "sipm" : 17,
        "slotGroup" : 7,
        "sipmGroup" : 6
        },
    1 : {
        "slots" : [23,24,25,26],
        "sipm" : 22,
        "slotGroup" : 9,
        "sipmGroup" : 8
        }
      }

JSlots = {
    1  : 0x18,
    2  : 0x19,
    3  : 0x1A,
    4  : 0x1B,
    5  : 0x1C,
    6  : 0x18,
    7  : 0x19,
    8  : 0x1A,
    9  : 0x1B,
    10 : 0x1C,
    17 : 0x18,
    18 : 0x19,
    19 : 0x1A,
    20 : 0x1B,
    21 : 0x1C,
    22 : 0x18,
    23 : 0x19,
    24 : 0x1A,
    25 : 0x1B,
    26 : 0x1C
         }
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

def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))

def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret

def getByteFromBits(bitList):
    return int(''.join(bitList), 2)
def getBytesFromBits(bitList):
    ret = []
    for i in xrange(len(bitList)/8):
        ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
    return ret


# class RM:
#     def __init__(self, rmNum):
#         self.sipm = RMs[rmNum]["sipm"]
#         self.slots = RMs[rmNum]["slots"]
#         self.cards = []
#         for i in slots:
#             self.cards.append(qCard(JSlots[i]))
#     def readIn(self):
#         for c in self.cards:
#             c.readIn()
#

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
            #autorange mode
            self.arr[38] = 1
        elif b == 0:
            #fixed range mode
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

################################################################################
