##############################
# Helpful Tool Functions
##############################

# give this function a string (like '133 4 92 23') and returns the binary cat
def strToBin(aString):
    j = 0
    catBinary = ""
    for i in aString.split():
        catBinary = catBinary + format(int(aString.split()[j]),'08b')
        j += 1
    return catBinary

# give a string (like '133 4 92 23') and returns those values in hex with spaces
def strToHex(string):
        catHex = ""
        j=0
        for i in string.split():
                catHex = catHex + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catHex

# give function a r/w indexed from sendBatch() and will determine if first
# value in the string is a non-zero error code
def isError(ret):
    if (ret[0] != '0'): # '0' is non-error value
        return True # error
    else:
        return False # no error

##############################
# Read/write functions
##############################
def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[1].split():
        ret.append(int(i))
    # print ret
    if isError(ret):
        #print "Error in read!"
        return False
    else:
        return ret[1:] #ignore the leading error code

# ------------------------------------------------------------------------

def writeToRegister(bus, address, register, toWrite):
    # toWrite can be the ret list from readFromRegister()
    bus.write(address, [register] + toWrite)
    ret = []
    for i in bus.sendBatch()[1].split():
        ret.append(int(i))
    if not isError(ret):
        return True # write successful
    else:
        return False # write failed

# ------------------------------------------------------------------------

def readWriteRead(bus, address, register, numBytes):
    read1 = readFromRegister(bus, address, register, numBytes)

    #if write is successful
    if (writeToRegister(bus,address, register,read1)):
        read2 = readFromRegister(bus, address, register, numBytes)
        if (read1 == read2):
            return True # R/W/R cycle gives identical reads, so PASS
        if (read1 != read2):
            # print "READ1 != READ2"
            return False # R/W/R cycle changed somehow, so FAIL
    #if write failed
    else:
        # print "WRITE FAILED IN R/W/R CYCLE"
        return False





##############################
# Library
##############################

iglooAdd = 0x09

igloo = {
    "fpgaMajVer" :{
        "address" : 0x00,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "fpgaMinVer" :{
        "address" : 0x01,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "ones" :{
        "address" : 0x02,
        "size" : 32,
        "RW" : 0,
        "expected" : "255 255 255 255"
        },
    "zeroes" :{
        "address" : 0x03,
        "size" : 32,
        "RW" : 0,
        "expected" : "0 0 0 0"
        },
    "fpgaTopOrBottom" :{
        "address" : 0x04,
        "size" : 8,
        "RW" : 0,
        "expected" : ""
        },
    "uniqueID" :{
        "address" : 0x05,
        "size" : 64,
        "RW" : 1,
        "expected" : ""
        },
    "statusReg" :{       # has its own internal register even deeper
        "address" : 0x10,
        "size" : 32,
        "RW" : 0,
        "expected" : "",
        },
    "cntrReg" :{         # has its own internal register even deeper
        "address" : 0x11,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "clk_count" :{
        "address" : 0x12,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "rst_QIE_count" :{
        "address" : 0x13,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "wte_count" :{
        "address" : 0x14,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "capIDErr_count" :{
        "address" : {
            "link1" : 0x15,
            "link2" : 0x16,
            "link3" : 0x17
                },
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "fifo_data" :{
        "address" : {
            "data1" : 0x30,
            "data2" : 0x31,
            "data3" : 0x32
                },
        "size" : 88,
        "RW" : 0,
        "expected" : ""
        },
    "inputSpy" :{
        "address" : 0x33,
        "size" : 200,
        "RW" : 0,
        "expected" : ""
        },
    "spy96Bits" :{
        "address" : 0x40,
        "size" : 96,
        "RW" : 0,
        "expected" : ""
        },
    "qie_ck_ph" :{
        "address" : {
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
        "address" : 0x80,
        "size" : 8,
        "RW" : 1,
        "expected" : ""
        },
    "link_test_pattern" :{
        "address" : 0x81,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "dataToSERDES" :{
        "address" : 0x82,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        },
    "addrToSERDES" :{
        "address" : : 0x83,
        "size" : 16,
        "RW" : 1,
        "expected" : ""
        },
    "ctrlToSERDES" :{
        "address" : 0x84,
        "size" : 8,
        "RW" : 1,
        "expected" : ""
        },
    "dataFromSERDES" :{
        "address" : 0x85,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        }
    "statFromSERDES" :{
        "address" : : 0x86,
        "size" : 32,
        "RW" : 0,
        "expected" : ""
        },
    "scratchReg" :{
        "address" : 0xFF,
        "size" : 32,
        "RW" : 1,
        "expected" : ""
        }
}
