from client import webBus
from Test import Test
import IglooLib

i = IglooLib


class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMajVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaMinVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMinVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ones(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ones"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class zeroes(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "zeroes"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaTopOrBottom(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaTopOrBottom"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class uniqueID(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "uniqueID"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RW = Writable~~"
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
        allRegList = i.readFromRegister(self.bus, i.iglooAdd, reg, size)
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

#        print "----------%s----------" %name
        self.read()

        if self.read() !=False:
            readPass = True

        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
#            print "~~PASS: RO not writable~~"
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
        allRegList = i.readFromRegister(self.bus, i.iglooAdd, reg, size)
        #print "allRegList: ", allRegList

        # if bad read
        if (allRegList == False): return False

        allRegBin = i.getBitsFromBytes(allRegList)
        allRegStr = i.catBitsFromBytes(allRegBin)

        cntrReg = {
        "31bX"             :   allRegStr[0:26],
        "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
        "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
        "2_bit_0"           :   allRegStr[28:30],
        "WrEn_InputSpy"     :   allRegStr[30:31],
        "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            }

        allReg = "31bx: " + cntrReg["31bX"] + '\n'\
             + "orbitHisto_clear: " + cntrReg["orbitHisto_clear"] + '\n'\
             + "orbitHisto_run: " + cntrReg["orbitHisto_run"] + '\n'\
             + "2_bit_0: " + cntrReg["2_bit_0"] + '\n'\
             + "WrEn_InputSpy: " + cntrReg["WrEn_InputSpy"] + '\n'\
             + "CI_mode: " + cntrReg["CI_mode"]

        # another option for readout instead of allReg is simply cntrReg (prints list)
        if desiredReg == "all":
            return allReg

        else:
            return cntrReg[desiredReg]

     # -------------------------------------------
    def testBody(self):
        readPass = False
        rwrPass = False

        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s Display----------" %name
        self.read()

        if self.read() !=False:
            readPass = True

        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            return True
        else:
            return False

# ------------------------------------------------------------------------
class cntrRegChange(Test): # NOTE: this run() function is overloaded to require parameters
     def testBody(self, desiredReg='CI_mode', settingStr='1'):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s Change----------" %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
#        print "settingStr: ", settingStr

        # Read1 = current register status
        read1 = i.readFromRegister(self.bus, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
#        print "allRegStr: ", allRegStr

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister(self.bus, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister(self.bus, i.iglooAdd, reg, size) # gets new reg status
#            print "cntrReg after 'all' WRITE: ", read2

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"             :   allRegStr[0:26],
            "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[28:30],
            "WrEn_InputSpy"     :   allRegStr[30:31],
            "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
                }

            #print "settingStr confirm: ", settingStr
            cntrReg[desiredReg] = settingStr
            #print "cntrReg[desiredReg]: ", cntrReg

            # Since Python is 'pass-by-object-reference', just because we changed
            # the dict cntrReg doesn't mean we changed allRegStr... So do that now
            #allRegStr = ''.join(cntrReg)
            allRegStr = cntrReg['31bX'] + cntrReg['orbitHisto_clear']\
                + cntrReg['orbitHisto_run'] + cntrReg["2_bit_0"]\
                + cntrReg['WrEn_InputSpy'] + cntrReg['CI_mode']

            #print "stringToBitList: ", i.stringToBitList(allRegStr)
            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            #print "toWrite: ", toWrite
            write1 = i.writeToRegister(self.bus, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister(self.bus, i.iglooAdd, reg, size) #displays new reg
#            print "cntrReg after %s WRITE: " %desiredReg, read2
            if not (write1 and read2): return False
            else:
                return True

    # -------------------------------------------
     def run(self, desiredReg='CI_mode', settingStr='1'):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg, settingStr) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
# ------------------------------------------------------------------------
class cntrRegTerminalChange(Test): # (NOT USED)
    # FILL THIS IN
    def testBody(self):
        return True
# ------------------------------------------------------------------------
class clk_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "clk_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class rst_QIE_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "rst_QIE_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class wte_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "wte_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RO count register, just test ability to read out
        if (i.readFromRegister(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class capIDErr_count(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "capIDErr_count"
        reg = [i.igloo[name]["register"]["link1"],\
            i.igloo[name]["register"]["link2"],i.igloo[name]["register"]["link3"]]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        linkPass = [False, False, False]

        # for RO count register, just test ability to read out
        link = 0
        for n in reg:
#            print '----Link',link+1,'----'
            if (i.readFromRegister(self.bus, i.iglooAdd, n, size)):
                linkPass[link] = True

            link = link + 1

        if (linkPass[0] and linkPass[1] and linkPass[2]):
#            print "~~ALL PASS: Read from RO~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fifo_data(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fifo_data"
        reg = [i.igloo[name]["register"]["data1"],\
            i.igloo[name]["register"]["data2"],i.igloo[name]["register"]["data3"]]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        dataPass = [False, False, False]

        # for RO register, read1 == read2 constitutes a PASS
        data = 0
        for n in reg:
#            print '----Data',data+1,'----'
            if (i.RWR_forRO(self.bus, i.iglooAdd, n, size)):
                dataPass[data] = True

            data = data + 1

        if (dataPass[0] and dataPass[1] and dataPass[2]):
#            print "~~ALL PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class inputSpy(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "inputSpy"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class spy96Bits(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "spy96Bits"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

#        print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class qie_ck_ph(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "qie_ck_ph"
        reg = [i.igloo[name]["register"][1],i.igloo[name]["register"][2],\
            i.igloo[name]["register"][3],i.igloo[name]["register"][4],\
            i.igloo[name]["register"][5],i.igloo[name]["register"][6],\
            i.igloo[name]["register"][7],i.igloo[name]["register"][8],\
            i.igloo[name]["register"][9],i.igloo[name]["register"][10],\
            i.igloo[name]["register"][11],i.igloo[name]["register"][12]]

        # for i in range(1,13):
        #     reg.append(i.igloo[name]["register"][str(i)])

        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        qiePass = [False,False,False,False,False,False,False,False,\
            False,False,False,False]

        # for RO register, read1 == read2 constitutes a PASS
        count = 0
        for n in reg:
#            print '----Qie',count+1,'----'
            if (i.RWR_withRestore(self.bus, i.iglooAdd, n, size)):
                qiePass[count] = True

            count = count + 1

        if (qiePass[0] and qiePass[1] and qiePass[2] and qiePass[3] and \
            qiePass[4] and qiePass[5] and qiePass[6] and qiePass[7] and \
            qiePass[8] and qiePass[9] and qiePass[10] and qiePass[11]):
#            print "~~ALL PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_mode(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "link_test_mode"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_pattern(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "link_test_pattern"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "dataToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

#        print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
#            print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class addrToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "addrToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ctrlToSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ctrlToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RW = Writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataFromSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "dataFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statFromSERDES(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "statFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RO not writable~~"
            return True
        else:
            return False
# ------------------------------------------------------------------------
class scratchReg(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "scratchReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

 #       print "----------%s----------" %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_withRestore(self.bus, i.iglooAdd, reg, size)):
 #           print "~~PASS: RW = Writable~~"
            return True
        else:
            return False

