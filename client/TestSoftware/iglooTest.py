'''
Goals:
* understand the "spy" register (probably the 200-bit one)
* try to write to a "read only" register and ensure that it didn't work
    * but first, read what's there so that in case you overwrite, you can undo your mistakes...
* understand the SERDES registers (see Microsemi documentation for meanings)
* create functions to read (and if possible) write to internal registers

'''
import sys
sys.path.append('../')
from client import webBus
import QIELib
b = webBus('pi5',0) #can add 'pi5,0' so won't print send/receive messages
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
        catHex = ""
        j=0
        for i in string.split():
                catHex = catHex + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catHex



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
    return strToHex(b.sendBatch()[1])

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
    return strToHex(b.sendBatch()[1])


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
    "InputSpyWordNum"   :   regBin[0:10], # number of words in InputSpyFifo (depth = 512)
    "InputSpyFifoEmpty" :   regBin[10],
    "InputSpyFifoFull"  :   regBin[11],
    "Qie_DLLNoLock"     :   regBin[12:24], # good when '0'
    "BRIDGE_SPARE"      :   regBin[24:30],
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
    "31'bX"   :   regBin[0:6],
    "orbitHisto_clear" :   regBin[6:12], # controls histo of the QIE_RST spacing
    "orbitHisto_run"  :   regBin[12:18], # controls histo of the QIE_RST spacing
    "2-bit 0"     :   regBin[18:20],
    "WrEn_InputSpy"      :   regBin[20:26],
    "CI_mode"             :   regBin[26:32], # Charge Injection mode of the QIE10
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
def wte_count(): # "WTE Counter" (Warning-test-enable signal for calibration purposes)
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
    "ClkCounter"  :   regBin[2:8], # 6-bit clock counter
    "QIE1_out"     :   regBin[8:24], # all QIE#_out are 16-bit
    "QIE2_out"      :   regBin[24:40],
    "QIE3_out"      :   regBin[40:56],
    "QIE4_out"      :   regBin[56:72],
    "QIE5_out"      :   regBin[72:88],
    "QIE6_out"      :   regBin[88:104],
    "QIE7_out"      :   regBin[104:120],
    "QIE8_out"      :   regBin[120:136],
    "QIE9_out"      :   regBin[136:152],
    "QIE10_out"      :   regBin[152:168],
    "QIE11_out"      :   regBin[168:184],
    "QIE12_out"      :   regBin[184:200],
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
    return strToHex(spy)

# Register bytes 0x60-6B (RW)
def qie_ck_ph(): # QIE1-12 Clock Phase (Valid values of 0-15)

    address = [0x61,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69,0x6A,0x6B]
    qie = []

    for i in range(0,12):
        b.write(0x09,[address[i]]) # clock phase for QIE#(i+1)
        b.read(0x09,1)

    batchArr = b.sendBatch()
    for i in range(0,24): #filling qie array
        if i%2 == 1:
            qie.append(strToHex(batchArr[i][1]))


    #formatting the output as a cat of the clock phases
    ret = ""
    for i in range(0,11):
        ret = ret + str((i+1)) + ": " + qie[i] + ", "
    ret = ret + "12: " + qie[11]

    return ret


##### Bytes 0x80-0x86: Registers related to data links ######

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
    b.write(0x09,[0x86])
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
def readAllIgloo():
    openIgloo(0,0)

    print 'FPGA Major Version: ' + fpgaMajVer()
    print 'FPGA Minor Version: ' + fpgaMinVer()
    print 'Ones: ' + ones()
    print 'Zeros: ' + zeros()
    print 'FPGATopOrBottom: ' + FPGATopOrBottom()
    print 'Unique ID: ' + uniqueID()
    print 'StatusReg: ' + statusReg()
    print 'CntrReg: ' + cntrReg()
    print 'Clock Counter: ' + clk_count()
    print 'QIE Reset Counter: ' + rst_QIE_count()
    print 'WTE Counter: ' + wte_count()
    print 'CapID Error Counter: ' + capIDErr_count()
    print 'FIFO Data: ' + fifo_data()
    print 'InputSpy: ' + inputSpy()
    print 'Spy96bits: ' + spy96bits()
    print 'QIE Clock Phase: ' + qie_ck_ph()
    print 'Link Test Mode: ' + link_test_mode()
    print 'Link Test Pattern: ' + link_test_pattern()
    print 'SERDES: ' + SERDES()
    print 'ScratchReg: ' + scratchReg()

readAllIgloo()

'''
OLD READOUT (WITH INCORRECT ARRAY CUTS INSIDE REGISTERS)---->>>

FPGA Major Version:  0
FPGA Minor Version:  9
Ones:  ff ff ff ff
Zeros: 0 0 0 0
FPGATopOrBottom: 0
Unique ID:  ad b 0 0 0 0 0 0
StatusReg: 000000010 : 0 : 0 : 00000010000 : 00000 : 0 : 0
CntrReg: 00000 : 00000 : 00000 : 0 : 00000 : 00000
Clock Counter:  40 1 85 75
QIE Reset Counter:  4 c8 79 1b
WTE Counter:  80 e7 79 1b
CapID Error Counter: Link1:  1 e 0 0, Link2:  1 e 0 0, Link3:  0 0 0 0
FIFO Data: Data1:  f0 4 4 4 4 4 6 ff ff ff ff, Data2:  f0 4 4 6 6 6 4 ff ff ff ff, Data3:  f4 4 4 4 4 4 5 ff ff ff ff
InputSpy: 0 : 0 : 00000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000000000000 : 000000001000000
Spy96bits:  0 0 0 0 0 0 0 0 0 0 a0 aa
QIE Clock Phase: QIE1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0
Link Test Mode:  0
Link Test Pattern:  ef be ed fe
SERDES: dataToSERDES:  0 0 0 0, addrToSERDES: 0000000000000000, ctrlToSERDES: 00000000, dataFromSERDES:  0 0 0 0, statFromSERDES:  0 0 0 0
ScratchReg:  ff ff ff ff


NEW READOUT (FIXED THE ARRAY CUTS)

FPGA Major Version:  0
FPGA Minor Version:  9
Ones:  ff ff ff ff
Zeros: 0 0 0 0
FPGATopOrBottom: 0
Unique ID:  ad b 0 0 0 0 0 0
StatusReg: 0000000100 : 0 : 0 : 000000100000 : 000000 : 0 : 0
CntrReg: 000000 : 000000 : 000000 : 00 : 000000 : 000000
Clock Counter:  8 a8 d8 30
QIE Reset Counter:  60 c8 d0 1b
WTE Counter:  22 e0 d0 1b
CapID Error Counter: Link1:  0 4 0 0, Link2:  0 4 0 0, Link3:  0 0 0 0
FIFO Data: Data1:  fc 5 5 5 5 4 5 ff ff ff ff, Data2:  f8 4 4 6 5 4 4 ff ff ff ff, Data3:  f0 4 4 6 4 4 5 ff ff ff ff
InputSpy: 0 : 0 : 000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000000000000 : 0000000010000000
Spy96bits:  0 0 0 0 0 0 0 0 0 0 a0 aa
QIE Clock Phase: QIE1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0
Link Test Mode:  0
Link Test Pattern:  ef be ed fe
SERDES: dataToSERDES:  0 0 0 0, addrToSERDES: 0000000000000000, ctrlToSERDES: 00000000, dataFromSERDES:  0 0 0 0, statFromSERDES:  0 0 0 0
ScratchReg:  ff ff ff ff
'''
