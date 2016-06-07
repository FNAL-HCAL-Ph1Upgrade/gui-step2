# Read UniqueID from QIE Card
from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

# Label RMs as 0, 1, 2, 3
# Label Slots as 0, 1, 2, 3

# Open Channel for QIE Card Given RM and Slot

def openChannel(rm,slot):
    if rm in [0,1]:
        # Open channel to ngCCM for RM 1,2: J1 - J10
        b.write(q.MUXs["fanout"],[0x02])
        b.sendBatch(b.messages)
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 3, 4: J17 - J26
        b.write(q.MUXs["fanout"],[0x01])
        b.sendBatch(b.messages)
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
    # Open channel to i2c group
    b.write(q.MUXs["ngccm"]["u10"], [q.RMi2c[rm]])
    b.sendBatch(b.messages)

# Read UniqueID
def uniqueID(rm,slot):
    openChannel(rm,slot)
    # Read UniqueID 8 bytes from SSN, U48 on QIE Card
    # Note that the i2c_select has register address 0x11
    # Note that the SSN expects 32 bits (4 bytes)
    b.write(q.QIEi2c[slot],[0x11,0x04,0,0,0])
    b.read(0x50,8)
    return b.sendBatch(b.messages)


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
