# Read UniqueID
def uniqueID(jslot):
    # Open channel to ngCCM for RM1,2, J1 - J12
    i2c_write(0x72,[0x02])
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])
    # Read UniqueID 8 bytes from SSN for first QIE in J2
    # Note that the i2c_select has register address 0x11
    # Note that the SSN expects 32 bits (4 bytes)
    i2c_write(0x19,[0x11,0x04,0,0,0])
    i2c_read(0x50,8)

def helloQIE(jslot):
    # Open channel to ngCCM for RM1,2, J1 - J12
    i2c_write(0x72,[0x02])
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])
    # Note that the QIEs for one half have register address 0x30
    # Note that the QIEs for the other half have register address 0x31
    # Note that the QIE expects 384 bits (48 bytes)
    # 384 bits = 64 bits * 6 qie cards = 8 bytes * 6 qie cards
    i2c_write(0x19,[0x30])
    i2c_read(0x30,48)

def getUniqueIDs():
