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
b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib

##############################
# Conversion Functions
##############################

#give this function a string (like '133 4 92 23') and returns the binary cat
def strToBin(aString):
    j = 0
    catBinary = ""
    for i in aString.split():
        catBinary = catBinary + format(int(aString.split()[j]),'08b')
        j += 1
    return catBinary

# helpful string to hex list
def strToHex(string):
        catBinary = ""
        j=0
        for i in string.split():
                catBinary = catBinary + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catBinary



##############################
# Igloo register functions
##############################

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
    return strToHex(majVer)

# Register byte 0x01 (RO)
def fpgaMinVer(): # "fpga minor verison"
    b.write(0x09,[0x01])
    b.read(0x09,1)
    minVer = b.sendBatch()[1]
    return strToHex(minVer)

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
def uniqueID(): # "should be written with QIE-card unique ID, powerup as 0xBAD"

    # I haven't added in writing to this register... will await Joe's declaration
    b.write(0x09,[0x05])
    b.read(0x09,8)
    return b.sendBatch()[1]


# Register byte 0x10 (RO)
# Status Register
def statusReg(desiredReg = "all"): # default = display all of register
    b.write(0x09, [0x10])
    b.read(0x09,4)
    reg = b.sendBatch()[1]

    #Now split up the 32 bits into their appropriate status chunks:
    #10-bit InputSpyWordNum, InputSpyFifoEmpty, InputSpyFifoFull,
    #Qie_DLLNoLock[12:1], BRIDGE_SPARE[5:0], 1-bit 0, PLL 320MHz Lock

    regBin = strToBin(reg)

    regBinDict = {
    "InputSpyWordNum"   :   regBin[0:9], # number of words in InputSpyFifo (depth = 512)
    "InputSpyFifoEmpty" :   regBin[10],
    "InputSpyFifoFull"  :   regBin[11],
    "Qie_DLLNoLock"     :   regBin[12:23], # good when '0'
    "BRIDGE_SPARE"      :   regBin[24:29],
    "1-bit"             :   regBin[30], # should be '0'
    "PLL 320MHz Lock"   :   regBin[31] # good when '1'
    }

    allRegBin = regBinDict["InputSpyWordNum"] + " : " + regBinDict["InputSpyFifoEmpty"]\
        + " : " + regBinDict["InputSpyFifoFull"] + " : " + regBinDict["Qie_DLLNoLock"]\
        + " : " + regBinDict["BRIDGE_SPARE"] + " : " + regBinDict["1-bit"]\
        + " : " + regBinDict["PLL 320MHz Lock"]

    if desiredReg == "all":
        return allRegBin
    else:
        return desiredReg + " = " + regBinDict[desiredReg]


# Register byte 0x11 (RW)
# Control Register
def cntrReg(desiredReg = "all"): # default = display all of register
    b.write(0x09, [0x11])
    b.read(0x09,4)
    reg = b.sendBatch()[1]

    #Now split up the 32 bits into their appropriate status chunks:
    #(I'm assuming 6-bit chunks and a 2-bit "zero" holder... Will adjust with more info)
    #31'bX, orbitHisto_clear, orbitHisto_run, 2-bit 0, WrEn_InputSpy, CI_mode

    regBin = strToBin(reg)

    regBinDict = {
    "31'bX"   :   regBin[0:5],
    "orbitHisto_clear" :   regBin[6:11], # controls histo of the QIE_RST spacing
    "orbitHisto_run"  :   regBin[12:17], # controls histo of the QIE_RST spacing
    "2-bit 0"     :   regBin[18:19],
    "WrEn_InputSpy"      :   regBin[20:25],
    "CI_mode"             :   regBin[26:31], # Charge Injection mode of the QIE10
    }

    allRegBin = regBinDict["31'bX"] + " : " + regBinDict["orbitHisto_clear"]\
        + " : " + regBinDict["orbitHisto_run"] + " : " + regBinDict["2-bit 0"]\
        + " : " + regBinDict["WrEn_InputSpy"] + " : " + regBinDict["CI_mode"]

    if desiredReg == "all":
        return allRegBin
    else:
        return desiredReg + " = " + regBinDict[desiredReg]


# Register byte 0x12 (RO)
def clk_count(): # "Clock Counter"
    b.write(0x09, [0x12])
    b.read(0x09,4)
    clkctr = b.sendBatch()[1]
    return strToHex(clkctr)

# Register byte 0x13 (RO)
def rst_QIE_count(): # "QIE Reset Counter"
    b.write(0x09, [0x13])
    b.read(0x09,4)
    rstctr = b.sendBatch()[1]
    return strToHex(rstctr)

# Register byte 0x14 (RO)
def wte_count(): # "WTE Counter"
    b.write(0x09, [0x14])
    b.read(0x09,4)
    wtectr = b.sendBatch()[1]
    return strToHex(wtectr)

# Register bytes 0x15-17 (RO)
def capIDErr_count(): # "Cap ID error Counter (Links 1-3)"
    b.write(0x09, [0x15]) # (link 1)
    b.read(0x09,4)
    link1 = b.sendBatch()[1]

    b.write(0x09, [0x16]) # (link 2)
    b.read(0x09,4)
    link2 = b.sendBatch()[1]

    b.write(0x09, [0x17]) # (link 3)
    b.read(0x09,4)
    link3 = b.sendBatch()[1]
    return "Link1: " + strToHex(link1) + ", Link2: " + strToHex(link1)\
        + ", Link3: " + strToHex(link3)

# Register bytes 0x30-32 (RO)
def fifo_data(): # "FIFO Data 1-3 (Reserved)"
    b.write(0x09, [0x30]) # (data1)
    b.read(0x09,11) # 88 bits = 11 bytes
    data1 = b.sendBatch()[1]

    b.write(0x09, [0x31]) # (data2)
    b.read(0x09,11)
    data2 = b.sendBatch()[1]

    b.write(0x09, [0x32]) # (data3)
    b.read(0x09,11)
    data3 = b.sendBatch()[1]
    return "Data1: " + strToHex(data1) + ", Data2: " + strToHex(data2)\
        + ", Data3: " + strToHex(data3)

# Register byte 0x33 (RO)
# Input Spy
def inputSpy(desiredReg = "all"): # default = display all of register
    b.write(0x09, [0x33])
    b.read(0x09,25) # 200 bits = 25 bytes
    reg = b.sendBatch()[1]

    #Now split up the 200 bits into their appropriate status chunks:
    #InputSpyFifoEmpty, InputSpyFifoFull, 6-bit ClkCounter, 16-bit QIE#_out * 12 for 12 cards

    regBin = strToBin(reg)

    regBinDict = {
    "InputSpyFifoEmpty"   :   regBin[0],
    "InputSpyFifoFull" :   regBin[1],
    "ClkCounter"  :   regBin[2:7], # 6-bit clock counter
    "QIE1_out"     :   regBin[8:23], # all QIE#_out are 16-bit
    "QIE2_out"      :   regBin[24:39],
    "QIE3_out"      :   regBin[40:55],
    "QIE4_out"      :   regBin[56:71],
    "QIE5_out"      :   regBin[72:87],
    "QIE6_out"      :   regBin[88:103],
    "QIE7_out"      :   regBin[104:119],
    "QIE8_out"      :   regBin[120:135],
    "QIE9_out"      :   regBin[136:151],
    "QIE10_out"      :   regBin[152:167],
    "QIE11_out"      :   regBin[168:183],
    "QIE12_out"      :   regBin[184:199],
    }

    allRegBin = regBinDict["InputSpyFifoEmpty"] + " : " + regBinDict["InputSpyFifoFull"]\
        + " : " + regBinDict["ClkCounter"] + " : " + regBinDict["QIE1_out"]\
        + " : " + regBinDict["QIE2_out"] + " : " + regBinDict["QIE3_out"]\
        + " : " + regBinDict["QIE4_out"] + " : " + regBinDict["QIE5_out"]\
        + " : " + regBinDict["QIE6_out"] + " : " + regBinDict["QIE7_out"]\
        + " : " + regBinDict["QIE8_out"] + " : " + regBinDict["QIE9_out"]\
        + " : " + regBinDict["QIE10_out"] + " : " + regBinDict["QIE11_out"]\
        + " : " + regBinDict["QIE12_out"]

    if desiredReg == "all":
        return allRegBin
    else:
        return desiredReg + " = " + regBinDict[desiredReg]

# Register byte 0x40 (RO)
# Spy96bits (pretty sure this is not used)
def spy96bits(): # "Fw-dependent monitoring (from v3.04 it is the orbit-histo)"
    b.write(0x09, [0x40])
    b.read(0x09,12) # 96 bits = 12 bytes
    spy = b.sendBatch()[1]
    return strToHex[spy]

# Register bytes 0x60-6B (RW)
def qie_ck_ph(): # QIE1-12 Clock Phase (Valid values of 0-15)
    b.write(0x09, [0x60]) # QIE1 clock phase
    b.read(0x09,1)
    qie1 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x61]) # QIE2
    b.read(0x09,1)
    qie2 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x62]) # QIE3
    b.read(0x09,1)
    qie3 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x63]) # QIE4
    b.read(0x09,1)
    qie4 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x64]) # QIE5
    b.read(0x09,1)
    qie5 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x65]) # QIE6
    b.read(0x09,1)
    qie6 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x66]) # QIE7
    b.read(0x09,1)
    qie7 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x67]) # QIE8
    b.read(0x09,1)
    qie8 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x68]) # QIE9
    b.read(0x09,1)
    qie9 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x69]) # QIE10
    b.read(0x09,1)
    qie10 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x6A]) # QIE11
    b.read(0x09,1)
    qie11 = strToHex(b.sendBatch()[1])

    b.write(0x09, [0x6B]) # QIE12
    b.read(0x09,1)
    qie12 = strToHex(b.sendBatch()[1])

    return "QIE1:" + qie1 + ", 2:" + qie2 + ", 3:" + qie3 + ", 4:" + qie4\
        + ", 5:" + qie5 + ", 6:" + qie6 + ", 7:" + qie7 + ", 8:" + qie8\
        + ", 9:" + qie9 + ", 10:" + qie10 + ", 11:" + qie11 + ", 12:" + qie12

# Register byte 0x80 (RW)
def link_test_mode():  # "Link test modes: hex7=ID, hex1=Counter-&-Pattern, hex0=Normal"
    b.write(0x09, [0x80])
    b.read(0x09,1)
    return strToHex(b.sendBatch()[1])

# Register byte 0x81 (RW)
def link_test_pattern(): # "Pattern to send during Counter-and-Pattern mode"
    b.write(0x09,[0x81])
    b.read(0x09,4)
    return strToHex(b.sendBatch()[1])

# Register byte 0x82 (RW)
def dataToSERDES(): # "SERDES APB_S_PWDATA"
    b.write(0x09,[0x82])
    b.read(0x09,4)
    return strToHex(b.sendBatch()[1])

# Register byte 0x83 (RW)
def addrToSERDES(): # "bits[13:2] tied to SERDES APB_S_PADDR[13:2]"
    b.write(0x09,[0x83])
    b.read(0x09,2)
    return strToBin(b.sendBatch()[1])

# Register byte 0x84 (RW)
def ctrlToSERDES(): # "bit0 = i2c_go, bit1 = i2c_write"
    b.write(0x09,[0x84])
    b.read(0x09,1)
    return strToBin(b.sendBatch()[1])

# Register byte 0x85 (RO)
def dataFromSERDES(): # "SERDES APB_S_PRDATA [31:0]"
    b.write(0x09,[0x85])
    b.read(0x09,4)
    return strToHex(b.sendBatch()[1])

# Register byte 0x86 (RO)
def statFromSERDES(): # "bit0 = busy, bit1 = i2c_counter"
    b.write(0x09,[0x82])
    b.read(0x09,4)
    return strToHex(b.sendBatch()[1])

# SERDES functions all together:
def SERDES():
    return "dataToSERDES: " + dataToSERDES() + ", addrToSERDES: " + addrToSERDES()\
        + ", ctrlToSERDES: " + ctrlToSERDES() + ", dataFromSERDES: " + dataFromSERDES()\
        + ", statFromSERDES: " + statFromSERDES()

# Register byte 0xFF (RW)
def scratchReg(): # "Scratch register"
    b.write(0x09,[0xFF])
    b.read(0x09, 4)
    return strToHex(b.sendBatch()[1])




#####################################################
# calling the functions
#####################################################

openIgloo(0,0)

print "FPGA Major Version: " + fpgaMajVer()
print "FPGA Minor Version: " + fpgaMinVer()
print "Ones: " + ones()
print "Zeros: " + zeros()
print "FPGATopOrBottom: " + FPGATopOrBottom()
print "Unique ID: " + uniqueID()
print "StatusReg: " + statusReg()
print "CntrReg: " + cntrReg()
print "Clock Counter: " + clk_count()
print "QIE Reset Counter: " + rst_QIE_count()
print "WTE Counter: " + wte_count()
print "CapID Error Counter: " + capIDErr_count()
print "FIFO Data: " + fifo_data()
print "InputSpy: " + inputSpy()
print "Spy96bits: " + spy96bits()
print "QIE Clock Phase: " + qie_ck_ph()
print "Link Test Mode: " + link_test_mode()
print "Link Test Pattern: " + link_test_pattern()
print "SERDES: " + SERDES()
print "ScratchReg: " + scratchReg()

##########################
# The Igloo2 class
##########################

#class Igloo:

    ###########################
    # Register Functions
    ###########################
