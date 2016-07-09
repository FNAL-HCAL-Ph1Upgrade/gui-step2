from client import webBus

##############################
# Helpful Tool Functions
##############################

# give function a !!REVERSED!! r/w indexed from sendBatch() and will determine
# if LAST value in the string is a non-zero error code
def isError(ret):
    if (ret[-1] != 0): # '0' is non-error value
        return True # error
    else:
        return False # no error

# takes decimal byte, returns list filled with exactly 8 bits
def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))

# give a list with decimal bytes, returns list of all bits
def getBitsFromBytes(decimalBytes):
    ret = []
    if not isinstance(decimalBytes, bool):
        for i in decimalBytes:
            ret = ret + getBitsFromByte(i)
    return ret

def getByteFromBits(bitList):
    return int(''.join(bitList), 2)

# give a list with bits (list size should be a multiple of 8), returns list of each formed byte
def getBytesFromBits(bitList):
    ret = []
    for i in xrange(len(bitList)/8):
        ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
    return ret

# give a string, returns list of each bit from string
def stringToBitList(stringOfBits):
    list = []
    for i in stringOfBits:
            list.append(i)

    return list

# give a list for binary, returns

# give a list of bits (from getBitsFromBytes()), cats into bit string based on cuts
# parameters:   bitList = list of bits
#               first = bit element to begin cat with
#               length = how many bits to cat after 'first'
def catBitsFromBytes(bitList, first = 0, length = 0):
    bitString = ""

    if (length == 0):
        for i in bitList:
            bitString = bitString + i

    elif (length > 0):
    	for i in bitList[first:(first+length)]:
    		bitString = bitString + i

    return bitString

# helpful string to hex list
def strToHex(string):
        catHex = ""
        j=0
        for i in string.split():
                catHex = catHex + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catHex



##############################
# Read/write functions
##############################

def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    # flip the bytes around (Bridge gives us LSB first... We want MSB first)
    ret.reverse()

    if isError(ret):
        print 'Read ERROR: '+str(ret)
        return False
    else:
        print 'Read Success: '+str(ret)
        return ret[:-1] #ignore the leading error code
# ------------------------------------------------------------------------
# quiet function, on successful read, returns without printing
def readFromRegister_Quiet(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    # flip the bytes around (Bridge gives us LSB first... We want MSB first)
    ret.reverse()

    if isError(ret):
        print 'Read ERROR: '+str(ret)
        return False
    else:
        return ret[:-1] #ignore the leading error code
# ------------------------------------------------------------------------

def writeToRegister(bus, address, register, toWrite):
    # toWrite can be the ret list from readFromRegister()
    toWrite.reverse()
    bus.write(address, [register] + toWrite)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    # flip the bytes around (Bridge gives us LSB first... We want MSB first)
    #ret.reverse()

    if not isError(ret):
        print 'Write Success: '+str(ret)
        return True # write successful
    else:
        print 'Write ERROR: '+str(ret)
        return False # write failed

# ------------------------------------------------------------------------

def writeToRegister_Quiet(bus, address, register, toWrite):
    # toWrite can be the ret list from readFromRegister()
    toWrite.reverse()
    bus.write(address, [register] + toWrite)
    ret = []
    for i in bus.sendBatch()[-1].split():
        ret.append(int(i))

    # flip the bytes around (Bridge gives us LSB first... We want MSB first)
    #ret.reverse()

    if not isError(ret):
        # print 'Write Success: '+str(ret)
        return True # write successful
    else:
        print 'Write ERROR: '+str(ret)
        return False # write failed

# ------------------------------------------------------------------------

# designed for easy **RW reg** use, so changes reg and then sets back to original
# ... if that cycle is successful (ie read1 != r2,and r1 = r3), then returns True
def RWR_withRestore(bus, address, register, numBytes):
    # Get read1
    read1 = readFromRegister(bus, address, register, numBytes)

    if read1 == False: return False

    augRead1 = [] # holds augmented read1
    for i in read1:
        if (i != 255): augRead1.append(i + 1)
        else: augRead1.append(i - 1)

    # Write different values to register
    w = writeToRegister(bus, address, register, augRead1)

    if w == False: return False

    # Get read2
    read2 = readFromRegister(bus, address, register, numBytes)

    #if write successully changed reg (aka read1 != read2)
    if (read1 != read2):
        # Write original values to register
        w = writeToRegister(bus, address, register, read1)

        read1.reverse() #write function flips bytes... Flip them back to compare with read3 properly

        if w == False: return False
        # Get read3
        read3 = readFromRegister(bus, address, register, numBytes)

        # if restored to original (aka read1 = read3)
        if read1 == read3:
            print 'Read1 = Read3 --> Reg changed, now restored to original'
            return True
        else:
            print 'Read1 != Read3'
            return False
    elif (read1 == read2):
        print 'Read1 = Read2 --> Write to RW Failed'
        return False


# ------------------------------------------------------------------------
def RWR_withRestore_Quiet(bus, address, register, numBytes):
    # Get read1
    read1 = readFromRegister_Quiet(bus, address, register, numBytes)

    if read1 == False: return False

    augRead1 = [] # holds augmented read1
    for i in read1:
        if (i != 255): augRead1.append(i + 1)
        else: augRead1.append(i - 1)

    # Write different values to register
    w = writeToRegister_Quiet(bus, address, register, augRead1)
    if w == False: return False

    # Get read2
    read2 = readFromRegister_Quiet(bus, address, register, numBytes)
    #if write successully changed reg (aka read1 != read2)
    if (read1 != read2):
        # Write original values to register
        w = writeToRegister_Quiet(bus, address, register, read1)

        read1.reverse() #write function flips bytes... Flip them back to compare with read3 properly
        if w == False: return False

        # Get read3
        read3 = readFromRegister_Quiet(bus, address, register, numBytes)
        # if restored to original (aka read1 = read3)
        if read1 == read3:
            # print 'Read1 = Read3 --> Reg changed, now restored to original'
            return True
        else:
            # print 'Read1 != Read3'
            return False
    elif (read1 == read2):
        # print 'Read1 = Read2 --> Write to RW Failed'
        return False


# ------------------------------------------------------------------------

# designed for easy **RO reg** use, so returns True when read1 = read2
def RWR_forRO(bus, address, register, numBytes):
    read1 = readFromRegister(bus, address, register, numBytes)

    if read1 == False: return False

    augRead1 = [] # augmented read1
    for i in read1:
        if (i != 255): augRead1.append(i + 1)
        else: augRead1.append(i - 1)

    #if write is successful
    if (writeToRegister(bus,address, register, augRead1)):
        read2 = readFromRegister(bus, address, register, numBytes)
        if (read1 == read2):
            print 'Read1 = Read2'
            return True # R/W/R cycle gives identical reads, so PASS
        if (read1 != read2):
            print 'READ1 != READ2'
            return False # R/W/R cycle changed somehow, so FAIL
    #if write failed
    else:
        print 'WRITE FAILED IN R/W/R CYCLE'
        return False
# ------------------------------------------------------------------------

# designed for easy **RO reg** use, so returns True when read1 = read2
def RWR_forRO_Quiet(bus, address, register, numBytes):
    read1 = readFromRegister_Quiet(bus, address, register, numBytes)

    if read1 == False: return False

    augRead1 = [] # augmented read1
    for i in read1:
        if (i != 255): augRead1.append(i + 1)
        else: augRead1.append(i - 1)

    #if write is successful
    if (writeToRegister_Quiet(bus,address, register, augRead1)):
        read2 = readFromRegister_Quiet(bus, address, register, numBytes)
        if (read1 == read2):
            # print 'Read1 = Read2'
            return True # R/W/R cycle gives identical reads, so PASS
        if (read1 != read2):
            # print 'READ1 != READ2'
            return False # R/W/R cycle changed somehow, so FAIL
    #if write failed
    else:
        # print 'WRITE FAILED IN R/W/R CYCLE'
        return False



##############################
# Library
##############################

iglooAdd = 0x09

#'size' is measured in bits

igloo = {
    "fpgaMajVer" :{
        "register" : 0x00,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "fpgaMinVer" :{
        "register" : 0x01,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "ones" :{
        "register" : 0x02,
        "size" : 32,
        "RW" : 0,
        "expected" : "255 255 255 255"
        },
    "zeroes" :{
        "register" : 0x03,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 0 0 0"
        },
    "fpgaTopOrBottom" :{
        "register" : 0x04,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "uniqueID" :{
        "register" : 0x05,
        "size" : 64,
        "RW" : 1,
        "expected" : ""
        },
    "statusReg" :{       # has its own internal register even deeper
        "register" : 0x10,
        "size" : 32,
        "RW" : 0,
        "expected" : "",
        },
    "cntrReg" :{         # has its own internal register even deeper
        "register" : 0x11,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "clk_count" :{
        "register" : 0x12,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "rst_QIE_count" :{
        "register" : 0x13,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "wte_count" :{
        "register" : 0x14,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "capIDErr_count" :{
        "register" : {
            "link1" : 0x15,
            "link2" : 0x16,
            "link3" : 0x17
                },
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "fifo_data" :{
        "register" : {
            "data1" : 0x30,
            "data2" : 0x31,
            "data3" : 0x32
                },
        "size" : 88,
        "RW" : 0,
        "expected" : ""
        },
    "inputSpy" :{
        "register" : 0x33,
        "size" : 200,
        "RW" : 0,
        "expected" : ""
        },
    "spy96Bits" :{
        "register" : 0x40,
        "size" : 96,
        "RW" : 0,
        "expected" : ""
        },
    "qie_ck_ph" :{
        "register" : {
            1 : 0x60,
            2 : 0x61,
            3 : 0x62,
            4 : 0x63,
            5 : 0x64,
            6 : 0x65,
            7 : 0x66,
            8 : 0x67,
            9 : 0x68,
            10: 0x69,
            11: 0x6A,
            12: 0x6B
                },
        "size" : 8,
        "RW" : 1,
        "expected" : ""
        },
    "link_test_mode" :{
        "register" : 0x80,
        "size" : 8,
        "RW" : 1,
        "expected" : ""
        },
    "link_test_pattern" :{
        "register" : 0x81,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "dataToSERDES" :{
        "register" : 0x82,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "addrToSERDES" :{
        "register" : 0x83,
        "size" : 16,
        "RW" : 1,
        "expected" : ""
        },
    "ctrlToSERDES" :{
        "register" : 0x84,
        "size" : 8,
        "RW" : 1,
        "expected" : ""
        },
    "dataFromSERDES" :{
        "register" : 0x85,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "statFromSERDES" :{
        "register"  : 0x86,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "scratchReg" :{
        "register" : 0xFF,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        }
}
