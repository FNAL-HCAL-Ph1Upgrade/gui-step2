# Read UniqueID from QIE Card
from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

# Label RMs as 0, 1, 2, 3
# Label Slots as 0, 1, 2, 3

# Open Channel for QIE Card Given RM and Slot
def send_clear():
    bus = b.sendBatch()
    b.clearBus()
    return bus

def openChannel(rm,slot):
    if rm in [0,1]:
        # Open channel to ngCCM for RM 1,2: J1 - J10
        print '##### RM in 0,1 #####'
        b.write(q.MUXs["fanout"],[0x02])
        send_clear()
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 3, 4: J17 - J26
        print '##### RM in 2,3 #####'
        b.write(q.MUXs["fanout"],[0x01])
        send_clear()
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
        return 'closed channel'
    # Open channel to i2c group
    print '##### open i2c #####'
    # b.clearBus()
    b.write(q.MUXs["ngccm"]["u10"], [q.RMi2c[rm]])
    return send_clear()

# Read UniqueID
def uniqueID(rm,slot):
    openChannel(rm,slot)
    # Read UniqueID 8 bytes from SSN, U48 on QIE Card
    # Note that the i2c_select has register address 0x11
    # Value : 4 = 0x04 (or 0x10 for Bit 4... we need to find out!)
    # Note that the SSN expects 32 bits (4 bytes)
    # The SSN may also expect 8 bits (1 byte) for write!
    print '##### Read UniqueID #####'
    b.write(q.QIEi2c[slot],[0x11,0x04,0,0,0])
    b.read(0x50,8)
    return send_clear()


# Read UniqueID for all QIE Cards in Backplane
# To read IDs for RM 1, pass RMList = [0]
# To read IDs for all RMS, pass RMList = [0, 1, 2, 3]
def getUniqueIDs(RMList):
    uniqueIDArray = range(4)
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = range(4)
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in range(4):
            idList[slot] = uniqueID(rm,slot)
        uniqueIDArray[rm] = idList
    return uniqueIDArray
