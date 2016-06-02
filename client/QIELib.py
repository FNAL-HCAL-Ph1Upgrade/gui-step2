#!/usr/bin/python
#
#QIELib.py
#Library of tables, functions, and classes for working with QIE11 test stands

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
        "slots" : ["J2", "J3", "J4", "J5"],
        "sipmC" : "J1",
        "slotGroup" : 2,
        "sipmGroup" : 1
        },
    3 : {
        "slots" : ["J7", "J8", "J9", "J10"],
        "sipmC" : "J6",
        "slotGroup" : 4,
        "sipmGroup" : 3
        },
    2 : {
        "slots" : ["J18", "J19", "J20", "J21"],
        "sipmC" : "J17",
        "slotGroup" : 7,
        "sipmGroup" : 6
        },
    1 : {
        "slots" : ["J23", "J24", "J25", "J26"],
        "sipmC" : "J22",
        "slotGroup" : 9,
        "sipmGroup" : 8
        }
      }

#For higher J, subtract 5
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

serialShiftRegisterBits = {
    "LVDS/SLVS" : [0],
    "P0, P1" : [1, 2],
    "DiscOn" : [3],
    "TGain" : [4],
    "TimingThresholdDAC" : [5,6,7,8,9,10,11,12],
    "TimingIref" : [13,14,15],
    "PedastalDAC" : [16,17,18,19,20,21],
    "CapID0pedastal" : [22,23,24,25],
    "CapID1pedastal" : [26,27,28,29],
    "CapID2pedastal" : [30,31,32,33],
    "CapID3pedastal" : [34, 35, 36, 37],
    "FixRange" : [38],
    "RangeSet" : [39, 30],
    "ChargeInjectDAC" : [41, 42, 43],
    "Gsel" : [44, 45, 46, 47, 48],
    "Idcset" : [49, 50, 51, 52, 53],
    "CkOutEn" : [54],
    "TDCmode" : [55],
    "Hsel" : [56],
    "PhaseDelay" : [57, 58, 59, 60, 61, 62, 63]
}

def getBits(decimal):
    return list('%05d' % int(bin(decimal)[2:]))

class shiftRegister:
    def __init__(self):
        self.QIEs = (QIE() for i in range(6))
    #returns a flattened array of all QIE register bits to be written as a block
    def flatten(self):
        '''flatten all of the bits in the register's QIEs to one list'''
        a = []
        for q in self.QIEs:
            for b in q.arr:
                a.append(b)
        return a
class QIE:
    def __init__(self):
        '''initialize a QIE11 object with default settings'''
        self.arr = list(0 for i in xrange(64))
        self.setToDefaults()
    def __repr__(self):
        return "QIE()"
    def __str__(self):
        '''Display each setting with values'''
        return "FooBar"

    def setToDefaults(self):
        #Defaults for following functions
        self.setLVDS()
        self.setLVDS_output_level_trim(350)
        self.discOn(0)
        self.TGain(0)
        self.TimingThresholdDAC(tuple(1 for i in xrange(8)))
        self.TimingIref(0)
        self.PedastalDAC(1, 6)
        self.ChargeInjectDAC(100)

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
        }.get(a)
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
    ##DEFAULT UNKNOWN
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
    def Gsel(t):
        for i in xrange(5):
            self.arr[44 + i] = t[i]

    #Change bits 49-53
    def Idcset():
        
    #Change bit 54
    def CkOutEn():

    #Change bit 55
    def TDCmode():

    #Change bit 56
    def Hsel():

    #Change bit 57-63
    def PhaseDelay():

    #Add print function, check each mode
