
# ###########################
# #### TABLE OF CONTENTS ####
# * client.py (webBus)
# * helpers.py
# * QIE.py
# * DaisyChain.py
# * DChains.py
# * Hardware.py
# ###########################



#############################################################################
# C L I E N T . P Y #########################################################
#############################################################################

#client.py
#client /library/ with which to send commands to server

#websocket (install websocket-client)
from websocket import create_connection

################################################################################
# webBus class
################################################################################

class webBus:
    def __init__(self, serverAddress = "pi5", VERBOSITY = 2):
        self.VERBOSITY = VERBOSITY
        self.messages = []
        a = "ws://%s:1738/ws" % serverAddress
        self.ws = create_connection(a)

    def read(self, address, numbytes):
        m = "r %i %i" % (address, numbytes)
        self.messages.append(m)

    def write(self, address, byteArray):
        m = "w %i " % address
        for h in byteArray:
            m += str(h) + " "
        self.messages.append(m)
    def sleep(self, n):
        m = "s %i" % n
        self.messages.append(m)
    def sendBatch(self):
        self.ws.send('|'.join(self.messages))
        ret = self.ws.recv().split('|')
        if self.VERBOSITY >= 1:
            for e in xrange(len(self.messages)):
                print "SENT: %s" % self.messages[e]
                print "RECEIVED: %s" % ret[e]
        self.messages = []
        return ret

################################################################################
if __name__ == "__main__":
    print "What you just ran is a library. Correct usage is to import this file\
    and use its class(es) and functions."



#############################################################################
# H E L P E R S . P Y #######################################################
#############################################################################



# helpers.py
# Helper functions for tests:

def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))
def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret
def getByteFromBits(bitList):
    return int(''.join(str(i) for i in bitList), 2)
def getBytesFromBits(bitList):
    ret = []
    for i in xrange(len(bitList)/8):
        ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
    return ret
def readBinaryRegister(bus, address, register, numBytes):
    return getBitsFromBytes(readFromRegister(bus, address, register, numBytes))
def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.sleep(1000)
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[2].split():
        ret.append(int(i))
    ret = ret[1:]
    return ret
def writeToRegister(bus, address, register, bytesToWrite):
    bus.write(address, [register] + list(bytesToWrite))
    return None
def toHex(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    s = ""
    return '0x' + s.join(message_list)

def reverseBytes(message):
    message_list = message.split()
    message_list.reverse()
    s = " "
    return s.join(message_list)







#############################################################################
# Q I E . P Y ###############################################################
#############################################################################


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
        }.get(q, (-9,-9,-9))
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


    ##############################################

    #Change bits 41-43
    def getChargeInjectDAC(self):
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
        }.get(charge, (-9,-9,-9))
        if d != (-9,-9,-9):
            for i in xrange(3):
                self[41 + i] = d[i]
        else:
            print "INVALID INPUT IN ChargeInjectDAC... no change made"









#############################################################################
# D A I S Y C H A I N . P Y #################################################
#############################################################################

#DaisyChain.py
#QIE DaisyChain class

# from QIE import QIE


class DaisyChain:
    def __init__(self, arr = list(0 for i in xrange(64 * 6))):
        '''creates a shift register object with 6 QIEs, default 0s'''
        self.QIEs = []
        for i in xrange(6):
            self.QIEs.append(QIE(arr[i * 64:(i + 1) * 64]))
        #Adry (6/24)
        # for i in xrange(6):
        #     self.CI.append(QIE(arr[]))
    def __repr__(self):
        return "DaisyChain()"
    def __str__(self):
        r = ""
        for q in self.QIEs:
            r += "-------\n"
            r += str(q)
            r += "\n"
            r += "-------\n"
        return r
    def __getitem__(self, i):
        return self.QIEs[i]
    #returns a flattened array of all QIE register bits to be written as a block
    def flatten(self):
        '''flatten all of the bits in the register's QIEs to one list'''
        a = []
        for q in self.QIEs:
            a += q.flatten()
        return a
    # def getCI(self):









#############################################################################
# D C H A I N S . P Y #######################################################
#############################################################################

#DChains.py

# from DaisyChain import DaisyChain
# from client import webBus
# from helpers import *
from optparse import OptionParser

class DChains:
    def __init__(self, address, bus):
        self.bus = bus
        self.chains = []
        self.address = address
    def read(self):
        for register in [0x30, 0x31]:
            self.chains.append(DaisyChain(readBinaryRegister(self.bus, self.address, register, 48)))
    def __str__(self):
        ret = ""
        for c in self.chains:
            ret += str(c)
        return ret
    def __getitem__(self, i):
        return self.chains[i/6][i % 6]
    def write(self):
        for i in range(2):
            register = [0x30, 0x31][i]
            writeToRegister(self.bus, self.address, register, getBytesFromBits(self.chains[i].flatten()))







#############################################################################
# H A R D W A R E . P Y #####################################################
#############################################################################

#Hardware.py
import sys
# from DChains import DChains

#MUX dict
  #Given JX, set MUXes
cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]
def getCardAddress(slot):
    if slot in [2,7,18,23] : return cardAddresses[0]
    if slot in [3,8,19,24] : return cardAddresses[1]
    if slot in [4,9,20,25] : return cardAddresses[2]
    if slot in [5,10,21,26]: return cardAddresses[3]

def getReadoutSlot(slot):
    if slot in [2,3,4,5] : return     4
    if slot in [7,8,9,10] : return    3
    if slot in [18,19,20,21] : return 2
    if slot in [23,24,25,26] : return 1
def ngccmGroup(rm):
    i2cGroups = [0x01, 0x10, 0x20, 0x02]
    return i2cGroups[rm-1]

def openChannel(slot, bus):
    rmLoc = getReadoutSlot(slot)
    if rmLoc in [3,4]:
      # Open channel to ngCCM for RM 3,4: J1 - J10
        bus.write(0x72,[0x02])
    elif rmLoc in [1,2]:
      # Open channel to ngCCM for RM 1,2: J17 - J26
        bus.write(0x72,[0x01])
    else:
        print 'Invalid RM = ', rmLoc
        print 'Please choose RM = {1,2,3,4}'
        return 'closed channel'
  # Open channel to i2c group
    bus.write(0x74, [ngccmGroup(rmLoc)])
    bus.read(0x74, 2)

  # Reset the backplane
    bus.write(0x00,[0x06])
    return bus.sendBatch()

#Get DChains
def getDChains(slot, bus):
    openChannel(slot, bus)
    return DChains(getCardAddress(slot), bus)

#SetQInjMode(t)
def SetQInjMode(onOffBit, slot, bus):
    openChannel(slot, bus)
    #expects onOffBit of 0 or 1
    if onOffBit == 0 or onOffBit == 1:
        bus.write(getCardAddress(slot),[0x11,0x03,0,0,0])
        bus.write(0x09,[0x11,onOffBit,0,0,0])
        bus.sendBatch()
    else:
        print "INVALID INPUT IN SetQInjMode... doing nothing"

# Cryptic 0x70 Reset
def reset(ngccm): #RM4,3->ngccm2 -- RM2,1->ngccm1
    b.write(0x72,[ngccm])
    b.write(0x74,[0x08])
    b.write(0x70,[0x3,0])
    b.write(0x70,[0x1,0])
    b.sendBatch()
