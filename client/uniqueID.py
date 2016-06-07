import QIELib

# Label RMs as 0, 1, 2, 3
# Label Slots as 0, 1, 2, 3

# Open Channel for QIE Card Given RM and Slot

def openChannel(rm,slot):
    if rm in [0,1]:
        # Open channel to ngCCM for RM 1,2: J1 - J10
        i2c_write(QIELib.MUXs["fanout"],[0x02])
    elif rm in [2,3]:
        # Open channel to ngCCM for RM 3, 4: J17 - J26
        i2c_write(QIELib.MUXs["fanout"],[0x01])
    else:
        print 'Invalid RM = ', rm
        print 'Please choose RM = {0,1,2,3}'
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])

# Read UniqueID
def uniqueID(rm,slot):
    if slot <= 13:
        # Open channel to ngCCM for RM 1,2: J1 - J12
        i2c_write(QIELib.MUXs["fanout"],[0x02])
    else:
        # Open channel to ngCCM for RM 3, 4: J17 - J26
        i2c_write(QIELib.MUXs["fanout"],[0x01])
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])
    # Read UniqueID 8 bytes from SSN for first QIE in J2
    # Note that the i2c_select has register address 0x11
    # Note that the SSN expects 32 bits (4 bytes)
    i2c_write(0x19,[0x11,0x04,0,0,0])
    i2c_read(0x50,8)

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
