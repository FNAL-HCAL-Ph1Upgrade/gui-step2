'''
Goals:
* understand the "spy" register (probably the 200-bit one)
* try to write to a "read only" register and ensure that it didn't work
    * but first, read what's there so that in case you overwrite, you can undo your mistakes...
* understand the SERDES registers (see Microsemi documentation for meanings)
* create functions to read (and if possible) write to internal registers

'''

from client import webBus
import QIELib
b = webBus("pi5") #can add "pi5,0" so won't print send/receive messages
q = QIELib


#give this function a string (like '133 4 92 23') and returns the binary cat
def strToBin(aString):
    j = 0
    catBinary = ""
    for i in aString.split():
        catBinary = catBinary + bin(int(aString.split()[j]))[2:]
        j += 1
    return catBinary


def openIgloo(rm,slot):
    q.openChannel(rm,slot)
    #the igloo is value "3" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
    b.sendBatch()


############################################################################
### NOTE: openIgloo(r,s) should already be called before these functions ###
############################################################################

# Register byte 0x00 (RO)
def fpgaMajVer(): # "fpga major version"
    b.write(0x09,[0x00])
    b.read(0x09,1)
    majVer = b.sendBatch()[1]
    print "majVer: " + majVer
    majVer = hex(int(majVer))[2:0]
    print "majVer in hex: " + majVer
    return majVer

# Register byte 0x01 (RO)
def fpgaMinVer(): # "fpga minor verison"
    b.write(0x09,[0x01])
    b.read(0x09,1)
    minVer = b.sendBatch()[1]
    minVer = hex(int(minVer))[2:0]
    return minVer

# Register byte 0x02 (RO)
def ones(): # "all ones register"
    b.write(0x09,[0x02])
    b.read(0x09,4)
    return b.sendBatch()[1]

# Register byte 0x03 (RO)
def zeros(): # "all zeros register"
    b.write(0x09,[0x03])
    b.read(0x09,4)
    return b.sendBatch()[1]

# Register byte 0x04 (RO)
def FPGATopOrBottom(): # "FPGA top or bottom bit"
    b.write(0x09,[0x04])
    b.read(0x09,1)
    return b.sendBatch()[1]


# Register byte 0x05 (R/W)
def uniqueID(): # "should be written with QIE-card unique ID"

    # I haven't added in writing to this register... will await Joe's declaration
    b.write(0x09,[0x05])
    b.read(0x09,8)
    return b.sendBatch()[1]

# Register byte 0x10 (RO)
def statusReg(desiredReg = "all"):
    b.write(0x09, [0x10])
    b.read(0x09,4)
    reg = b.sendBatch()[1]
    
    #split up the 32 bits into their appropriate status chunks:
    #10-bit InputSpyWordNum, InputSpyFifoEmpty, InputSpyFifoFull,
    #Qie_DLLNoLock[12:1], BRIDGE_SPARE[5:0], 1-bit 0, PLL 320MHz Lock
    
    regBin = strToBin(reg)
    
    return regBin

    '''
    regBinDict = {
    "InputSpyWordNum"   :   regBin[0:9], # number of words in InputSpyFifo (depth = 512)
    "InputSpyFifoEmpty" :   regBin[10],
    "InputSpyFifoFull"  :   regBin[11],
    "Qie_DLLNoLock"     :   regBin[12:23], # good when '0'
    "BRIDGE_SPARE"      :   regBin[24:29],
    "1-bit"             :   regBin[30], # should be '0'
    "PLL 320MHz Lock"   :   regBin[31] # good when '1'
    }

    allRegBin = regBin[0:9] + " : " + regBin[10] + " : " + regBin[11]\
        + " : " + regBin[12:23] + " : " + regBin[24:29] + " : " + regBin[30]\
        + " : " + regBin[31]
    '''
'''
    if desiredReg == "all":
        return allRegBin
    else:
        return desiredReg + " = " + regBinDict[desiredReg]
'''

openIgloo(0,0)
print statusReg()

#print "FPGA Major Version: " + fpgaMajVer()
print "RegBin: " + statusReg()


##########################
# The Igloo2 class
##########################

#class Igloo:

    ###########################
    # Register Functions
    ###########################
