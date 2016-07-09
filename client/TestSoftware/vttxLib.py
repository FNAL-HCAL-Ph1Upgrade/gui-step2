from client import webBus
#b = webBus("pi6",0)

######################################################
# VTTX Dict
######################################################

# size is in BYTES
vttx = {
    "i2c_select" : {
        1 : [0x01, 0,0,0],
        2 : [0x02, 0,0,0]
        },
    "address"   : 0x7E,
    "size"      : 7      #size of register in bytes
}

######################################################
# Helpful tool functions
######################################################

def isError(ret):
    if (ret[0] != 0): # '0' is non-error value
        return True # error
    else:
        return False # no error

# helpful string decimal to string hex
def strToHex(string):
        catBinary = ""
        j=0
        for i in string.split():
                catBinary = catBinary + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catBinary

######################################################
# Read/write functions
######################################################
def openVTTX(slot, vttxNum):
    b.write(slot,[0x11] + vttx["i2c_select"][vttxNum])
    b.sendBatch()

def readFromVTTX(bus, address, numBytes):
    bus.write(address, [0x00])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    if isError(ret):
        print 'Read ERROR: '+str(ret)
        return False
    else:
 #       print 'Read Success: '+str(ret)
        return ret[1:] #ignore the leading error code

def writeToVTTX(bus, address, numBytes, toWrite):
    # toWrite can be the ret list from readFromRegister()
    bus.write(address, [0x00] + toWrite)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    if not isError(ret):
 #       print 'Write Success: '+str(ret)
        return True # write successful
    else:
        print 'Write ERROR: '+str(ret)
        return False # write failed

# Read from Vttx1, write something else, read again to confirm
def RWR_withRestore(bus, address, numBytes):
    # Get read1
    read1 = readFromVTTX(bus, address, numBytes)

    if read1 == False: return False

    augRead1 = [] # holds augmented read1
    for i in read1:
        if (i != 255): augRead1.append(i + 1)
        else: augRead1.append(i - 1)

    # Write different values to register
    w = writeToVTTX(bus, address, numBytes, augRead1)
    if w == False: return False

    # Get read2
    read2 = readFromVTTX(bus, address, numBytes)
    #if write successully changed reg (aka read1 != read2)
    if (read1 != read2):
        # Write original values to register
        w = writeToVTTX(bus, address, numBytes, read1)
        if w == False: return False
        # Get read3
        read3 = readFromVTTX(bus, address, numBytes)
        # if restored to original (aka read1 = read3)
        if read1 == read3:
#           print 'Read1 = Read3 --> Reg changed, now restored to original'
            return True
        else:
#            print 'Read1 != Read3'
            return False
    elif (read1 == read2):
#        print 'Read1 = Read2 --> Write to RW Failed'
        return False
