#TestLib.py
#Testing Library for QIE Tests.
 
from client import webBus
import QIELib
#b = webBus("pi5")
#q = QIELib
 
#MUX slave addresses (slave i2c addresses)
MUXs = {
    "fanout" : 0x72,
    "ngccm" : {
                "u10" : 0x74,
                "u18" : 0x70
                },
    "bridge" : [0x19, 0x1a, 0x1b, 0x1c]
        }
#Register addresses
REGs = {
    "qie0" : 0x30,
    "qie1" : 0x31,
    "iscSelect" : 0x11,
    "vttx" : 0x7E,
    "igloo" : 0x09,
    "ID" : 0x50,
    "temp" : 0x40
        }
# Simplify your life today with RMi2c and QIEi2c. Boom dog.
 
RMi2c = {
    0 : 0x02,
    1 : 0x20,
    2 : 0x10,
    3 : 0x01
        }
 
QIEi2c = {
    0 : 0x19,
    1 : 0x1a,
    2 : 0x1b,
    3 : 0x1c
        }
 
######## Bridge Test Function Dictionary
 
# Bridge Register Tests
 
def idString(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
def idStringCont(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
def fwVersion(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
def ones(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
def zeroes(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
def onesZeroes(slot,address):
    b.write(q.QIEi2c[slot],[adress])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]
 
bridgeDict = {
    0 : {
        'function' : idString,
        'address' : 0x00,
    },
    1 : {
        'function' : idStringCont,
        'address' : 0x01,
    },
    2 : {
        'function' : fwVersion,
        'address' : 0x04,
    },
    3 : {
        'function' : ones,
        'address' : 0x08,
    },
    4 : {
        'function' : zeroes,
        'address' : 0x09,
    },
    5 : {
        'function' : onesZeroes,
        'address' : 0x0A,
    },
}
 
######## open channel to RM and Slot! ######################
 
def openChannel(rm,slot):
    if rm in [0,1]:
        # Open channel to ngCCM for RM 1,2: J1 - J10
        print '##### RM in 0,1 #####'
        b.write(q.MUXs["fanout"],[0x02])
        b.sendBatch()
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 3, 4: J17 - J26
        print '##### RM in 2,3 #####'
        b.write(q.MUXs["fanout"],[0x01])
        b.sendBatch()
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
        return 'closed channel'
    # Open channel to i2c group
    print '##### open i2c #####'
    # b.clearBus()
    b.write(q.MUXs["ngccm"]["u10"], [q.RMi2c[rm]])
    return b.sendBatch()
 
# Print UniqueID Arrary
# RN = Registration Number
# SN = Serial Number
def printIDs(uniqueIDArray):
    print
    for rm in xrange(len(uniqueIDArray)):
        for slot in xrange(len(uniqueIDArray[0])):
            revRN = reverseBytes(uniqueIDArray[rm][slot])
            hexRN = toHex(revRN)
            revSN = serialNum(revRN)
            hexSN = toHex(revSN)
            print 'RM: ', rm, ' slot: ', slot
            # print 'Unique Registration Number (dec): ', revRN
            # print 'Unique Registration Number (hex): ', hexRN
            # print 'Serial Number (dec): ', revSN
            print 'Serial Number (hex): ', hexSN
            print
 
# Reverse order of string of bytes separated by spaces.
def reverseBytes(message):
    message_list = message.split()
    message_list.reverse()
    s = " "
    return s.join(message_list)
 
# Convert string of ints with spaces to a string of hex values with no spaces... one long string.
def toHex(message,colon=0):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    if colon:
        s = ":"
        return s.join(message_list)
    s = ""
    return '0x' + s.join(message_list)
 
# Parse Serial Number from 8 byte Registration Number.
def serialNum(message):
    message_list = message.split()
    message_list = message_list[1:-1]
    s = " "
    return s.join(message_list)
 
#ASCII
def toASCII(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = chr(int(message_list[byte]))
    s = ""
    return s.join(message_list)
