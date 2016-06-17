from client import webBus
import QIELib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib

##############################
# Helpful Tool Functions
##############################

# # give this function a string (like '133 4 92 23') and returns the binary cat
# def strToBin(aString):
#     j = 0
#     catBinary = ""
#     for i in aString.split():
#         catBinary = catBinary + format(int(aString.split()[j]),'08b')
#         j += 1
#     return catBinary
#
# # give a string (like '133 4 92 23') and returns those values in hex with spaces
# def strToHex(string):
#         catHex = ""
#         j=0
#         for i in string.split():
#                 catHex = catHex + " " + hex(int(string.split()[j]))[2:]
#                 j = j + 1
#         return catHex

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

    print ret

    if isError(ret):
        print "Error in read!"
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
        print "Write Success"
        return True # write successful
    else:
        print "Write Fail"
        return False # write failed

# ------------------------------------------------------------------------

def readWriteRead(bus, address, register, numBytes):
    read1 = readFromRegister(bus, address, register, numBytes)

    #if write is successful
    if (writeToRegister(bus,address, register,read1)):
        read2 = readFromRegister(bus, address, register, numBytes)
        if (read1 == read2):
            print "Read1 = read2"
            return True # R/W/R cycle gives identical reads, so PASS
        if (read1 != read2):
            print "READ1 != READ2"
            return False # R/W/R cycle changed somehow, so FAIL
    #if write failed
    else:
        print "WRITE FAILED IN R/W/R CYCLE"
        return False





##############################
# Library
##############################

iglooAdd = 0x09

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
