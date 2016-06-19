from client import webBus
import QIELib
import IglooLib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib
i = IglooLib


class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logfile #changed from logstream to logfile
        self.iterations = iterations
    def run(self):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody() == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
    def log(self, message):
        logprint(message, file=self.logfile)
    def testBody(self):
        return True

# ------------------------------------------------------------------------
class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMajVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaMinVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMinVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ones(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ones"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class zeroes(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "zeroes"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaTopOrBottom(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaTopOrBottom"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class uniqueID(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "uniqueID"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statusReg(Test): #inherit from Test class, overload testBody() function
    # -------------------------------------------

    def read(self, desiredReg = "all"):
        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister(b, i.iglooAdd, reg, size)
        #print "allRegList: ", allRegList

        # if bad read
        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        statusReg = {
            "InputSpyWordNum"   :   allRegStr[0:10], # number of words in InputSpyFifo (depth = 512)
            "InputSpyFifoEmpty" :   allRegStr[10],
            "InputSpyFifoFull"  :   allRegStr[11],
            "Qie_DLLNoLock"     :   allRegStr[12:24], # good when '0'
            "BRIDGE_SPARE"      :   allRegStr[24:30],
            "1_bit"             :   allRegStr[30], # should be '0'
            "PLL_320MHz_Lock"   :   allRegStr[31] # good when '1'
                }

        allReg = statusReg["InputSpyWordNum"] + " : " + statusReg["InputSpyFifoEmpty"]\
            + " : " + statusReg["InputSpyFifoFull"] + " : " + statusReg["Qie_DLLNoLock"]\
            + " : " + statusReg["BRIDGE_SPARE"] + " : " + statusReg["1_bit"]\
            + " : " + statusReg["PLL_320MHz_Lock"]

        if desiredReg == "all":
            return allReg

        else:
            return statusReg[desiredReg]

    # -------------------------------------------
    def testBody(self):
        readPass = False
        rwrPass = False

        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s----------" %name
        print self.read()

        if self.read() !=False:
            readPass = True

        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(b, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class cntrRegDisplay(Test): #inherit from Test class, overload testBody() function
    # -------------------------------------------
    def read(self, desiredReg = "all"):
        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister(b, i.iglooAdd, reg, size)
        #print "allRegList: ", allRegList

        # if bad read
        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        cntrReg = {
        "31bX"             :   allRegStr[0:6],
        "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
        "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
        "2_bit_0"           :   allRegStr[18:20],
        "WrEn_InputSpy"     :   allRegStr[20:26],
        "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
            }

        allReg = "31bx: " + cntrReg["31bX"] + '\n'\
             + "orbitHisto_clear: " + cntrReg["orbitHisto_clear"] + '\n'\
             + "orbitHisto_run: " + cntrReg["orbitHisto_run"] + '\n'\
             + "2_bit_0: " + cntrReg["2_bit_0"] + '\n'\
             + "WrEn_InputSpy: " + cntrReg["WrEn_InputSpy"] + '\n'\
             + "CI_mode: " + cntrReg["CI_mode"]

        if desiredReg == "all":
            return allReg

        else:
            return cntrReg[desiredReg]

    # -------------------------------------------
    # def write(self, desiredReg, settingList):
    #     name = "cntrReg"
    #     reg = i.igloo[name]["register"]
    #     size = i.igloo[name]["size"] / 8
    #
    #     # READ FIRST
    #     read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
    #
    #     if (read1 == False): return False
    #
    #     #makes read1 (byte list) into a bit string
    #     allRegStr = ''.join(i.catBitsFromBytes(i.getBitsFromBytes(read1)))
    #
    #     settingStr = ''.join(settingList)
    #     toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
    #
    #     # WRITE, THEN READ AGAIN TO SEE CHANGES
    #     if desiredReg == "all":
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 =i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'if': WRITE1/READ2 ERROR"
    #             return False
    #
    #     else:
    #         cntrReg = {
    #         "31bX"             :   allRegStr[0:6],
    #         "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
    #         "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
    #         "2_bit_0"           :   allRegStr[18:20],
    #         "WrEn_InputSpy"     :   allRegStr[20:26],
    #         "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
    #             }
    #
    #         cntrReg[desiredReg] = settingStr
    #
    #         toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'else': WRITE1/READ2 ERROR"
    #             return False

    # packed away: old interactive write() function
    {
    # -------------------------------------------
    # in theory, you can make string parameter settingList = ['000000', '11', '001001', etc]"
    # and it will join the elements and assign them to appropriate settings
    # in cntrReg...
    # def write(self, desiredReg, settingList):
    #     name = "cntrReg"
    #     reg = i.igloo[name]["register"]
    #     size = i.igloo[name]["size"] / 8
    #
    #     # READ FIRST
    #     read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
    #
    #     if (read1 == False): return False
    #
    #     #makes read1 (byte list) into a bit string
    #     allRegStr = ''.join(i.catBitsFromBytes(i.getBitsFromBytes(read1)))
    #
    #     settingStr = ''.join(settingList)
    #     toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
    #
    #     # WRITE, THEN READ AGAIN TO SEE CHANGES
    #     if desiredReg == "all":
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 =i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'if': WRITE1/READ2 ERROR"
    #             return False
    #
    #     else:
    #         cntrReg = {
    #         "31bX"             :   allRegStr[0:6],
    #         "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
    #         "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
    #         "2_bit_0"           :   allRegStr[18:20],
    #         "WrEn_InputSpy"     :   allRegStr[20:26],
    #         "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
    #             }
    #
    #         cntrReg[desiredReg] = settingStr
    #
    #         toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
    #         write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the user-input new reg
    #         read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
    #
    #         if not (write1 and read2):
    #             print "In 'else': WRITE1/READ2 ERROR"
    #             return False
    }

    # -------------------------------------------
    def testBody(self):
        readPass = False
        rwrPass = False

        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s Display----------" %name
        print self.read()

        if self.read() !=False:
            readPass = True

        if (i.RWR_withRestore(b, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            return True
        else:
            return False

        # desiredReg = raw_input("Enter cntrReg name (enter=all, 'more'=ShowNames): ")
        # if desiredReg == '': desiredReg = 'all'
        # elif desiredReg == 'more':
        #     print "31bX, " + "orbitHisto_clear, " + "orbitHisto_run, "\
        #         + "2_bit_0, " + "WrEn_InputSpy, " + "CI_mode"
        #     desiredReg = raw_input("Enter cntrReg name: ")
        #     if desiredReg == '': desiredReg = 'all'
        #
        # settingList = raw_input("Enter cntrReg setting list ['n1','n2', ...]: ")
        #
        # self.write(desiredReg, settingList)

        # for RO register, read1 == read2 constitutes a PASS
        # NEED TO CHANGE THIS FOR CNTRREG SINCE WE EXPECT TO R/W NON-RAND VALUES!!
# ------------------------------------------------------------------------
class cntrRegChange(Test):
    # -------------------------------------------
    def writeSet(self, desiredReg, settingStr):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print "----------%s Change----------" %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
        print "settingStr: ", settingStr

        # Read1 = current register status
        read1 = i.readFromRegister(b, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
        print "allRegStr: ", allRegStr

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister(b, i.iglooAdd, reg, size) # gets new reg status
            print "cntrReg after 'all' WRITE: ", read2

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"              :   allRegStr[0:6],
            "orbitHisto_clear"  :   allRegStr[6:12], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[12:18], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[18:20],
            "WrEn_InputSpy"     :   allRegStr[20:26],
            "CI_mode"           :   allRegStr[26:32], # Charge Injection mode of the QIE10
                }

            print "settingStr confirm: ", settingStr
            cntrReg[desiredReg] = settingStr
            print "cntrReg[desiredReg]: ", cntrReg

            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            write1 = i.writeToRegister(b, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister(b, i.iglooAdd, reg, size) #displays new reg
            print "cntrReg after %s WRITE: " %desiredReg, read2
            if not (write1 and read2): return False
            else:
                return True
    def testBody(self):
        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        return True
        #print "----------%s Change----------" %name
        #print self.writeSet()

        #if self.writeSet() != False:
        #    return True
# ------------------------------------------------------------------------
class cntrRegTerminalChange(Test): #inherit from Test class, overload testBody() function
    # FILL THIS IN
    def testBody(self):
        return True
# ------------------------------------------------------------------------
def runAll():
    def openIgloo(rm,slot):
        q.openChannel(rm,slot)
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0,0)

    m = fpgaMajVer(b,i.igloo["fpgaMajVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaMinVer(b,i.igloo["fpgaMinVer"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = ones(b,i.igloo["ones"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = zeroes(b,i.igloo["zeroes"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = fpgaTopOrBottom(b,i.igloo["fpgaTopOrBottom"]["register"],'iglooClass.txt', 1)
    print m.run()
    m = uniqueID(b,i.igloo["uniqueID"]["register"],'iglooClass.txt', 2)
    print m.run()
    m = statusReg(b,i.igloo["statusReg"]["register"],'iglooClass.txt', 2)
    print m.run()
    m = cntrRegDisplay(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 2)
    print m.run()
    m = cntrRegChange(b,i.igloo["cntrReg"]["register"],'iglooClass.txt', 2)
    m.writeSet("CI_mode", "111111")
    print m.run()

runAll()

# make sys.arg changes so taht when you run iglooClass.py from the terminal,
# it will take "options" like user-input, with the default being just run
# basic r/w capabilities.

# ALSO, make a rwr test for RW registers that returns all the register to the
# original values from read1 so that we don't make permanent changes we don't
# intend to make.

# Make 3 classes for cntrReg:
# (1) read out reg, (2) write according to hard-code, (3) write by terminal input
# in the runAll() function, put all three and comment in/out as desired
# the 1st option (read) should probably be done preceding any every write


# RW functions to do cursory RW test:
#   * uniqueID
#   * qie_ck_ph
#   * link_test_mode
#   * link_test_pattern
#   * dataToSERDES
#   * addrToSERDES
#   * ctrlToSERDES
#   * scratchReg
# RW functions to allow setting changes:
#   * cntrReg
