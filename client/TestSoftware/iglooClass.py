import IglooLib
import Hardware as h
import helpers as t
from Test import Test
import time

i = IglooLib

slot = 18 # the J_# slot

# ------------------------------------------------------------------------
class fpgaMajVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMajVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            maj = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)
            if maj == [0]:
                print maj
                print '~~PASS: Igloo Major Ver Firmware = 0 ~~'
                return True
            else:
                print '~~FAIL: Igloo Minor Ver Mismatch ~~'
                return False
        else:
            return False
# ------------------------------------------------------------------------
class fpgaMinVer(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaMinVer"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            min = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)
            if min == [9]:
                print min
                print '~~PASS: Igloo Minor Ver Firmware = 9 ~~'
                return True
            else:
                print '~~FAIL: Igloo Minor Ver Mismatch ~~'
                return False
        else:
            return False
# ------------------------------------------------------------------------
class ones(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "ones"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS

        if (i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size) == [255,255,255,255]):
        # if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
        #     print '~~PASS: RO not writable~~'
            print '~~PASS: all ones~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class zeroes(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "zeroes"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size) == [0,0,0,0]):
        # if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
        #     print '~~PASS: RO not writable~~'
            print '~~PASS: all zeroes~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fpgaTopOrBottom(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "fpgaTopOrBottom"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class uniqueID(Test): #inherit from Test class, overload testBody() function
    def testBody(self):
        name = "uniqueID"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statusReg(Test): #shows status register settings
    # -------------------------------------------

    def read(self, desiredReg = "all"):
        name = "statusReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)
        #print 'allRegList: '+str(allRegList)

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

        allReg = "InputSpyWordNum: " + statusReg["InputSpyWordNum"] + '\n'\
             + "InputSpyFifoEmpty: " + statusReg["InputSpyFifoEmpty"] + '\n'\
             + "InputSpyFifoFull: " + statusReg["InputSpyFifoFull"] + '\n'\
             + "Qie_DLLNoLock: " + statusReg["Qie_DLLNoLock"] + '\n'\
             + "BRIDGE_SPARE: " + statusReg["BRIDGE_SPARE"] + '\n'\
             + "1_bit: " + statusReg["1_bit"] + '\n'\
             + "PLL_320MHz_Lock: " + statusReg["PLL_320MHz_Lock"]

        # allReg = statusReg["InputSpyWordNum"] + " : " + statusReg["InputSpyFifoEmpty"]\
        #     + " : " + statusReg["InputSpyFifoFull"] + " : " + statusReg["Qie_DLLNoLock"]\
        #     + " : " + statusReg["BRIDGE_SPARE"] + " : " + statusReg["1_bit"]\
        #     + " : " + statusReg["PLL_320MHz_Lock"]

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

        print '----------%s----------' %name
        print self.read()

        if self.read() !=False:
            readPass = True

        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False

# ------------------------------------------------------------------------
class Igloo2_FPGA_Control(Test):
    def testBody(self):
        print '~~ Begin Toggle Igloo Power Slave'
        control_address = 0x22
        message = self.readBridge(control_address,4)
        print 'Igloo Control = '+str(message)

        ones_address = 0x02
        all_ones = '255 255 255 255'

        	retval = False

        self.bus.write(0x00,[0x06])
        self.bus.sendBatch()

        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
            retval = False
        print 'Igloo Ones = '+str(register)

        # Turn Igloo Off
        print 'Igloo Control = '+str(self.toggleIgloo())
        register = self.detectIglooError(ones_address, 4)
        if register[0] != '0':
            retval = True
        print 'Igloo Ones = '+str(register)

        # Turn Igloo On
        print 'Igloo Control = '+str(self.toggleIgloo())
        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
            retval = False
        print 'Igloo Ones = '+str(register)
        if retval:
            print '~~ Toggle Igloo Power PASS'
        else:
            print '~~ Toggle Igloo Power FAIL'
        return retval

    def toggleIgloo(self):
        iglooControl = 0x22
        message = self.readBridge(iglooControl,4)
        value = t.getValue(message)
        value = value ^ 0x400 # toggle igloo power!
        messageList = t.getMessageList(value,4)
        self.writeBridge(iglooControl,messageList)
        return self.readBridge(iglooControl,4)

    def writeBridge(self, regAddress, messageList):
        self.bus.write(0x19, [regAddress]+messageList)
        return self.bus.sendBatch()

    def readBridge(self, regAddress, num_bytes):
        self.bus.write(0x00,[0x06])
        self.bus.sendBatch()
        self.bus.write(0x19,[regAddress])
        self.bus.read(0x19, num_bytes)
        message = self.bus.sendBatch()[-1]
        if message[0] != '0':
            print 'Bridge i2c error detected'
        return t.reverseBytes(message[2:])

	def readIgloo(self, regAddress, num_bytes):
		self.bus.write(0x00,[0x06])
		self.bus.write(self.address,[0x11,0x03,0,0,0])
		self.bus.write(0x09,[regAddress])
		self.bus.read(0x09, num_bytes)
		message = self.bus.sendBatch()[-1]
		if message[0] != '0':
			print 'Igloo i2c error detected in readIgloo'
		return t.reverseBytes(message[2:])

	def detectIglooError(self, regAddress, num_bytes):
		self.bus.write(0x00,[0x06])
		self.bus.write(self.address,[0x11,0x03,0,0,0])
		self.bus.write(0x09,[regAddress])
		self.bus.read(0x09, num_bytes)
		message = self.bus.sendBatch()[-1]
		if message[0] != '0':
			print 'Igloo Power Off Confirmed.'
		return message

# ------------------------------------------------------------------------

class cntrRegDisplay(Test): #shows control register settings
    # -------------------------------------------
    def read(self, desiredReg = "all"):
        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        allRegList = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)
        #print 'allRegList: '+str(allRegList)

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

        allReg = "31bx: " + cntrReg["31bX"] + '\n' + "orbitHisto_clear: " + cntrReg["orbitHisto_clear"] + '\n'+ "orbitHisto_run: " + cntrReg["orbitHisto_run"] + '\n'+ "2_bit_0: " + cntrReg["2_bit_0"] + '\n'+ "WrEn_InputSpy: " + cntrReg["WrEn_InputSpy"] + '\n'+ "CI_mode: " + cntrReg["CI_mode"]

        # another option for readout instead of allReg is simply cntrReg (prints list)
        if desiredReg == "all":
            return allReg

        else:
            return cntrReg[desiredReg]

    def testBody(self, desiredReg):
        readPass = False
        rwrPass = False

        name = "cntrReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s Display----------' %name
        print self.read(desiredReg)

        if self.read(desiredReg) !=False:
            readPass = True

        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            rwrPass = True

        if (readPass and rwrPass):
            return True
        else:
            return False

    def run(self, desiredReg = 'all'):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes)
# ------------------------------------------------------------------------
class cntrRegChange(Test): # NOTE: this run() function is overloaded to require parameters
    # -------------------------------------------
    def testBody(self, desiredReg, settingStr):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s Change----------' %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
        print 'settingStr: '+str(settingStr)

        # Read1 = current register status
        read1 = i.readFromRegister(self.bus, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
        print 'allRegStr: '+str(allRegStr)

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister(self.bus, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister(self.bus, i.iglooAdd, reg, size) # gets new reg status
            print 'cntrReg after '"all"' WRITE: '+str(read2)

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"              :   allRegStr[0:26],
            "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[28:30],
            "WrEn_InputSpy"     :   allRegStr[30:31],
            "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
                }
            # cntrReg = {
            # "31bX"             :   allRegStr[0:26],
            # "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            # "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            # "2_bit_0"           :   allRegStr[28:30],
            # "WrEn_InputSpy"     :   allRegStr[30:31],
            # "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            #     }

            #print 'settingStr confirm: '+str(settingStr)
            cntrReg[desiredReg] = settingStr
            #print 'cntrReg[desiredReg]: '+str(cntrReg)

            # Since Python is 'pass-by-object-reference', just because we changed
            # the dict cntrReg doesn't mean we changed allRegStr... So do that now
            #allRegStr = ''.join(cntrReg)
            allRegStr = cntrReg['31bX'] + cntrReg['orbitHisto_clear']\
                + cntrReg['orbitHisto_run'] + cntrReg["2_bit_0"]\
                + cntrReg['WrEn_InputSpy'] + cntrReg['CI_mode']

            #print 'stringToBitList: '+str(i.stringToBitList(allRegStr))
            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            #print 'toWrite: '+str(toWrite)
            write1 = i.writeToRegister(self.bus, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister(self.bus, i.iglooAdd, reg, size) #displays new reg
            print 'cntrReg after %s WRITE: ' %desiredReg+str(read2)
            if not (write1 and read2): return False
            else:
                return True

    # -------------------------------------------
    def run(self, desiredReg, settingStr):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg, settingStr) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
# ------------------------------------------------------------------------
class cntrRegChange_Quiet(Test): # NOTE: this run() function is overloaded to require parameters
    # -------------------------------------------
    def testBody(self, desiredReg, settingStr):
        # desiredReg and settingStr are both strings!!
        # settingStr can be of form "010101...", "0101 111 0 11...", or "0101"
        name = 'cntrReg'
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s Change----------' %name

        settingStr = ''.join(settingStr)
        toWrite = i.getBytesFromBits(i.stringToBitList(settingStr))
        # print 'settingStr: '+str(settingStr)

        # Read1 = current register status
        read1 = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)
        allRegStr = i.catBitsFromBytes(i.getBitsFromBytes(read1))
        # print 'allRegStr: '+str(allRegStr)

        # Write to 'all' ---------------------------------------------------
        if desiredReg == "all":
            write1 = i.writeToRegister_Quiet(self.bus, i.iglooAdd, reg, toWrite)
            read2 = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size) # gets new reg status
            # print 'cntrReg after 'all' WRITE: '+str(read2)

            if not (write1 and read2): return False
            else:
                return True

        # Write to specific setting ----------------------------------------
        else:
            cntrReg = {
            "31bX"              :   allRegStr[0:26],
            "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            "2_bit_0"           :   allRegStr[28:30],
            "WrEn_InputSpy"     :   allRegStr[30:31],
            "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
                }
            # cntrReg = {
            # "31bX"             :   allRegStr[0:26],
            # "orbitHisto_clear"  :   allRegStr[26:27], # controls histo of the QIE_RST spacing
            # "orbitHisto_run"    :   allRegStr[27:28], # controls histo of the QIE_RST spacing
            # "2_bit_0"           :   allRegStr[28:30],
            # "WrEn_InputSpy"     :   allRegStr[30:31],
            # "CI_mode"           :   allRegStr[31:32], # Charge Injection mode of the QIE10
            #     }

            #print 'settingStr confirm: '+str(settingStr)
            cntrReg[desiredReg] = settingStr
            #print 'cntrReg[desiredReg]: '+str(cntrReg)

            # Since Python is 'pass-by-object-reference', just because we changed
            # the dict cntrReg doesn't mean we changed allRegStr... So do that now
            #allRegStr = ''.join(cntrReg)
            allRegStr = cntrReg['31bX'] + cntrReg['orbitHisto_clear']\
                + cntrReg['orbitHisto_run'] + cntrReg["2_bit_0"]\
                + cntrReg['WrEn_InputSpy'] + cntrReg['CI_mode']

            #print 'stringToBitList: '+str(i.stringToBitList(allRegStr))
            toWrite = i.getBytesFromBits(i.stringToBitList(allRegStr))
            #print 'toWrite: '+str(toWrite)
            write1 = i.writeToRegister_Quiet(self.bus, i.iglooAdd, reg, toWrite) #writes the change
            read2 = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size) #displays new reg
            # print 'cntrReg after %s WRITE: ' %desiredReg+str(read2)
            if not (write1 and read2): return False
            else:
                return True

    # -------------------------------------------
    def run(self, desiredReg, settingStr):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(desiredReg, settingStr) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
# ------------------------------------------------------------------------
class clk_count(Test): #clock count
    def testBody(self):
        name = "clk_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        sleepFactor=0.25

        print '----------%s----------' %name
        resultArr=[]
        diffGoodVal = True
        for n in xrange(2):
            resultArr.append(t.getValue(i.intListToString(i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size))))
            diff = 0
            if n != 0:
                diff = resultArr[n] - resultArr[n-1]
                if diff < 0: diff += 2**32
                rate = (float(diff)/(sleepFactor))
                if rate > 41000000 or rate < 40000000: # approx 40MHz clock frequency
                    diffGoodVal = False
                print rate
            time.sleep(1*sleepFactor)
        if (diffGoodVal):
            print '~~ Pass: Clk Count 40MHz ~~'
            return True
        else:
            print '~~ Fail: Clk Count NOT 40MHz ~~'
            return False
# ------------------------------------------------------------------------
class rst_QIE_count(Test): #reset qie count
    def testBody(self):
        name = "rst_QIE_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        sleepFactor=0.25

        print '----------%s----------' %name
        resultArr=[]
        diffGoodVal = True
        for n in xrange(2):
            resultArr.append(t.getValue(i.intListToString(i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size))))
            diff = 0
            if n != 0:
                diff = resultArr[n] - resultArr[n-1]
                if diff < 0: diff += 2**32
                rate = (float(diff)/(sleepFactor))
                if rate > 12500 or rate < 10500: # approx 11kHz
                    diffGoodVal = False
                print rate
            time.sleep(1*sleepFactor)
        if (diffGoodVal):
            print '~~ Pass: RST Counter 11kHz ~~'
            return True
        else:
            print '~~ Fail: Counter NOT 11kHz ~~'
            return False
# ------------------------------------------------------------------------
class wte_count(Test): #warning-test-enable count
    def testBody(self):
        name = "wte_count"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8
        sleepFactor = 0.25

        print '----------%s----------' %name
        resultArr=[]
        diffGoodVal = True
        for n in xrange(2):
            resultArr.append(t.getValue(i.intListToString(i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size))))
            diff = 0
            if n != 0:
                diff = resultArr[n] - resultArr[n-1]
                if diff < 0: diff += 2**32
                rate = (float(diff)/(sleepFactor))
                if rate > 59000 or rate < 15000: # approx 37kHz
                    diffGoodVal = False
                print rate
            time.sleep(1*sleepFactor)
        if (diffGoodVal):
            print '~~ Pass: WTE Counter 37kHz ~~'
            return True
        else:
            print '~~ Fail: Counter NOT 37kHz ~~'
            return False
# ------------------------------------------------------------------------
class capIDErr_count(Test): # changed: deleted obselete Link 3
    def testBody(self):
        name = "capIDErr_count"
        reg = [i.igloo[name]["register"]["link1"],\
            i.igloo[name]["register"]["link2"]]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        linkPass = [False, False]

        link = 0
        for count,n in enumerate(reg):
            print '----Link'+str(link+1)+'----'
            read1 = i.readFromRegister_Quiet(self.bus, i.iglooAdd, n, size)
            if (read1):
                linkPass[link] = True

            link = link + 1

        if (linkPass[0] and linkPass[1]):
            print '~~ALL PASS: Read from RO~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class fifo_data(Test): #NOTE: Unused register
    def testBody(self):
        name = "fifo_data"
        reg = [i.igloo[name]["register"]["data1"],\
            i.igloo[name]["register"]["data2"],i.igloo[name]["register"]["data3"]]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        dataPass = [False, False, False]

        # for RO register, read1 == read2 constitutes a PASS
        data = 0
        for n in reg:
            print '----Data'+str(data+1)+'----'
            if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, n, size)):
                dataPass[data] = True

            data = data + 1

        if (dataPass[0] and dataPass[1] and dataPass[2]):
            print '~~ALL PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class inputSpy(Test): #NOTE: run() takes parameter (default provided); processes Spy Buffer Data with bitwise operations
    # NOTE: run() takes parameter for total fifo extractions from InputSpy. Default = 512 (full test)
    # -------------------------------------------
    def run(self, fifoIterations=512):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody(fifoIterations) == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes)

    # -------------------------------------------
    def testBody(self, fifoIterations):
        # Set total numbers of iterations (512 for full testing of InputSpy)
        name = "inputSpy"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print '----------%s----------' %name
        passCount_512 = 0 # maximum = 512
        prevCapId = []

        for iter in range(0, fifoIterations):
            print '___________'
            print 'ITER: '+str(iter)
            capIdPass          = False
            adcPass            = False

            buff = i.readFromRegister_Quiet(self.bus, i.iglooAdd, reg, size)

            # if good read
            if (buff) != False:
                buff.reverse() # InputSpy doesn't flip bytes like Bridge does

            # Get InputSpy data (qieList = [capIdConcise, adc, rangeQ, tdc])
                qieList = self.printData(buff)

            # Check CapID
                # print 'prevCapId: '+str(prevCapId)
                if self.checkCapId(qieList[0], prevCapId, iter):
                    print '~~CapIDs Rotate~~'
                    capIdPass = True
                else:
                    print 'CapId Rotation ERROR: '+str(prevCapId)+' -> '+str(qieList[0])
                    capIdPass = False

            # Check ADC
                if self.checkAdc(qieList[1]):
                    print '~~ADC Good Zone~~'
                    adcPass = True
                else:
                    print 'ADC Too High ERROR'

                if (capIdPass and adcPass): passCount_512 += 1

                prevCapId = qieList[0]
                # print '\n'

            # if bad read
            else: print 'ERROR: Cannot Read Buffer, ITER: '+str(iter)

        # return after 512 iterations
        if passCount_512 == fifoIterations:
            print '~~ ALL %d PASS ~~' %fifoIterations
            return True
        else:
            print '>> Pass Count (out of 512): '+str(passCount_512)+' <<'
            return False

    # -------------------------------------------
    def interleave(self, c0, c1):
        retval = 0;
        for i in range(0,8):
            bitmask = 0x01 << i
            retval |= ((c0 & bitmask) | ((c1 & bitmask) << 1)) << i

        return retval
    # -------------------------------------------
    def printData(self,buff): # returns: qieList = [capIdConcise, adc, rangeQ, tdc]
        # buff holds 25 bytes (first 24)
        pedArray = [] # dimensions: pedArray[12][4]
        for x in xrange(12):
            row = []
            for y in xrange(4):
                row.append(-1)
            pedArray.append(row)

        BITMASK_TDC = 0x07 # const char
        OFFSET_TDC  = 4 # const int
        BITMASK_ADC = 0x07 # const char
        OFFSET_ADC  = 1 # const int
        BITMASK_EXP = 0x01 # const char
        OFFSET_EXP  = 0 # const int
        BITMASK_CAP = 0x01 # const char
        OFFSET_CAP  = 7 # const int

        fifoEmpty = buff[24] & 0x80
        fifoFull  = buff[24] & 0x40
        clkctr    = buff[24] & 0x3f
        adc     = []
        tdc     = []
        capId   = []
        rangeQ  = []

        for i in range(0,12):

            adc1 = (buff[(11-i)*2 + 1] >> OFFSET_ADC) & BITMASK_ADC
            adc0 = (buff[(11-i)*2    ] >> OFFSET_ADC) & BITMASK_ADC
            tdc1 = (buff[(11-i)*2 + 1] >> OFFSET_TDC) & BITMASK_TDC
            tdc0 = (buff[(11-i)*2    ] >> OFFSET_TDC) & BITMASK_TDC
            cap1 = (buff[(11-i)*2 + 1] >> OFFSET_CAP) & BITMASK_CAP
            cap0 = (buff[(11-i)*2    ] >> OFFSET_CAP) & BITMASK_CAP
            exp1 = (buff[(11-i)*2 + 1] >> OFFSET_EXP) & BITMASK_EXP
            exp0 = (buff[(11-i)*2    ] >> OFFSET_EXP) & BITMASK_EXP

            adc.append(self.interleave(adc0, adc1))
            tdc.append(self.interleave(tdc0, tdc1))
            capId.append(self.interleave(cap0, cap1))
            rangeQ.append(self.interleave(exp0, exp1))

            pedArray[i][0x03 & int(capId[i])] += int(0x3f & adc[i])

        print 'FIFO empty: %1d   FIFO full: %1d   clk counter: %6d' % (fifoEmpty,fifoFull,clkctr)
        print '       '


        capIdConcise = []
        for i in capId:
            capIdConcise.append(i & 0x03)

        print 'CapID: '+str(capIdConcise)
        print 'ADC:   '+str(adc)
        print 'RANGE: '+str(rangeQ)
        print 'TDC:   '+str(tdc)
        # print '\n'

        qieList = [capIdConcise, adc, rangeQ, tdc]

        return qieList
    # -------------------------------------------
    def checkCapId(self, capId, prevCapId, iter):
        allSamePass = True
        rotatePass  = True
        checkList = [capId[0]]*12
        rotateList = []

        # check that all 12 chips are same capId
        count = 0
        for i in capId:
            if (i != checkList[count]):
                allSamePass = False
            count += 1


        if iter != 0: # if a legit prevCapId exists
            for i in prevCapId:
                if i != 3: rotateList.append(i+1)
                elif i == 3: rotateList.append(0)
            # if prevCapId[0]   == 0:   rotateList = [1]*12
            # elif prevCapId[0] == 1:   rotateList = [2]*12
            # elif prevCapId[0] == 2:   rotateList = [3]*12
            # elif prevCapId[0] == 3:   rotateList = [0]*12
                else: print 'PrevCapId out of Scope 0-3'

            if capId != rotateList:
                rotatePass = False

        # return (allSamePass and rotatePass)
        return rotatePass

    # -------------------------------------------
    def checkAdc(self, adc):
        goodValPass = True

        for i in adc:
            if i >= 100:
                print 'Bad ADC Value: '+str(i)
                goodValPass = False

        return goodValPass
# ------------------------------------------------------------------------
class inputSpyRWR(Test): #NOTE: confirms RO nature of reg... doesn't process Spy Buffer
    def testBody(self):
        name = "inputSpy"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print '----------%s RWR----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class inputSpy_512Reads(Test): #flips bits in cntrReg then calls inputSpy() 512x
    def testBody(self):
    # turn WrEn_InputSpy ON
        myCntrRegChange = cntrRegChange_Quiet(self.bus,i.igloo["cntrReg"]["register"], 1)
        print myCntrRegChange.run('WrEn_InputSpy', '1')
    # turn WrEn_InputSpy OFF
        myCntrRegChange = cntrRegChange_Quiet(self.bus,i.igloo["cntrReg"]["register"], 1)
        print myCntrRegChange.run('WrEn_InputSpy', '0')
    # Read out InputSpy 512x
        myInputSpy = inputSpy(self.bus,i.igloo["inputSpy"]["register"], 1)
        runReturn = myInputSpy.run(512)
        if runReturn == (1,0):
            return True
        else:
            return False
# ------------------------------------------------------------------------
class spy96Bits(Test): #reads out orbit-histo data (diagnostic against same Bridge data)
    def testBody(self):
        name = "spy96Bits"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8      # dict holds bits, we want bytes

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class qie_ck_ph(Test): #NOTE: Uninterested in register at this time
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

        print '----------%s----------' %name
        qiePass = [False,False,False,False,False,False,False,False,\
            False,False,False,False]

        # for RO register, read1 == read2 constitutes a PASS
        count = 0
        for n in reg:
            print '----Qie'+str(count+1)+'----'
            if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, n, size)):
                qiePass[count] = True

            count = count + 1

        if (qiePass[0] and qiePass[1] and qiePass[2] and qiePass[3] and \
            qiePass[4] and qiePass[5] and qiePass[6] and qiePass[7] and \
            qiePass[8] and qiePass[9] and qiePass[10] and qiePass[11]):
            print '~~ALL PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_mode(Test): #NOTE: Uninterested in register at this time
    def testBody(self):
        name = "link_test_mode"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class link_test_pattern(Test): #NOTE: Uninterested in register at this time
    def testBody(self):
        name = "link_test_pattern"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataToSERDES(Test): #NOTE: Will not test at this time
    def testBody(self):
        name = "dataToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class addrToSERDES(Test): #NOTE: Will not test at this time
    def testBody(self):
        name = "addrToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class ctrlToSERDES(Test): #NOTE: Will not test at this time
    def testBody(self):
        name = "ctrlToSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RW register, read1 != read2 constitues a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class dataFromSERDES(Test): #NOTE: Will not test at this time
    def testBody(self):
        name = "dataFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class statFromSERDES(Test): #NOTE: Will not test at this time
    def testBody(self):
        name = "statFromSERDES"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_forRO_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RO not writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class scratchReg(Test): #
    def testBody(self):
        name = "scratchReg"
        reg = i.igloo[name]["register"]
        size = i.igloo[name]["size"] / 8

        print '----------%s----------' %name
        # for RO register, read1 == read2 constitutes a PASS
        if (i.RWR_withRestore_Quiet(self.bus, i.iglooAdd, reg, size)):
            print '~~PASS: RW = Writable~~'
            return True
        else:
            return False
# ------------------------------------------------------------------------
class CI_Mode_On(Test): # turns on Charge Injection on card
    def testBody(self):
        myCntrRegChange = cntrRegChange_Quiet(self.bus,i.igloo["cntrReg"]["register"], 1)
        print myCntrRegChange.run('CI_mode', '1')
        myDisplay = cntrRegDisplay(self.bus,i.igloo["cntrReg"]["register"], 1)
        if (myDisplay.read('CI_mode') == '1'):
            print '~~PASS: CI_mode set to ON~~'
            return True
        else:
            print 'ERROR: Cannot change CI to ON'
# ------------------------------------------------------------------------
class CI_Mode_Off(Test): # turns off Charge Injection on card
    def testBody(self):
        myCntrRegChange = cntrRegChange_Quiet(self.bus,i.igloo["cntrReg"]["register"], 1)
        print myCntrRegChange.run('CI_mode', '0')
        myDisplay = cntrRegDisplay(self.bus,i.igloo["cntrReg"]["register"], 1)
        if (myDisplay.read('CI_mode') == '0'):
            print '~~PASS: CI_mode set to OFF~~'
            return True
        else:
            print 'ERROR: Cannot change CI to OFF'
# ------------------------------------------------------------------------
class CI_Mode_Display(Test): # turns off Charge Injection on card
    def testBody(self):
        myDisplay = cntrRegDisplay(self.bus,i.igloo["cntrReg"]["register"], 1)
        if (myDisplay.read('CI_mode') == '1'):
            print '~~CI_mode is ON~~'
            return True
        elif (myDisplay.read('CI_mode') == '0'):
            print '~~CI_mode is OFF~~'
            return True
        else:
            print 'ERROR: Cannot read CI_mode'
# ------------------------------------------------------------------------

def runAll(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])

    m = fpgaMajVer(bus,i.igloo["fpgaMajVer"]["register"], 1)
    print m.run()
    m = fpgaMinVer(bus,i.igloo["fpgaMinVer"]["register"], 1)
    print m.run()
    m = ones(bus,i.igloo["ones"]["register"], 1)
    print m.run()
    m = zeroes(bus,i.igloo["zeroes"]["register"], 1)
    print m.run()
    m = fpgaTopOrBottom(bus,i.igloo["fpgaTopOrBottom"]["register"], 1)
    print m.run()
    m = uniqueID(bus,i.igloo["uniqueID"]["register"], 1)
    print m.run()
    m = statusReg(bus,i.igloo["statusReg"]["register"], 1)
    print m.run()
    m = cntrRegDisplay(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()
    m = cntrRegChange(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run('all', '')
    m = clk_count(bus,i.igloo["clk_count"]["register"], 1)
    print m.run()
    m = rst_QIE_count(bus,i.igloo["rst_QIE_count"]["register"], 1)
    print m.run()
    m = wte_count(bus,i.igloo["wte_count"]["register"], 1)
    print m.run()
    m = capIDErr_count(bus,i.igloo["capIDErr_count"]["register"], 1)
    print m.run()
    m = fifo_data(bus,i.igloo["fifo_data"]["register"], 1)
    print m.run()
    m = inputSpy(bus,i.igloo["inputSpy"]["register"], 1)
    print m.run()
    m = spy96Bits(bus,i.igloo["spy96Bits"]["register"], 1)
    print m.run()
    m = qie_ck_ph(bus,i.igloo["qie_ck_ph"]["register"], 1)
    print m.run()
    m = link_test_mode(bus,i.igloo["link_test_mode"]["register"], 1)
    print m.run()
    m = link_test_pattern(bus,i.igloo["link_test_pattern"]["register"], 1)
    print m.run()
    m = dataToSERDES(bus,i.igloo["dataToSERDES"]["register"], 1)
    print m.run()
    m = addrToSERDES(bus,i.igloo["addrToSERDES"]["register"], 1)
    print m.run()
    m = ctrlToSERDES(bus,i.igloo["ctrlToSERDES"]["register"], 1)
    print m.run()
    m = dataFromSERDES(bus,i.igloo["dataFromSERDES"]["register"], 1)
    print m.run()
    m = statFromSERDES(bus,i.igloo["statFromSERDES"]["register"], 1)
    print m.run()
    m = scratchReg(bus,i.igloo["scratchReg"]["register"], 1)
    print m.run()

def runSelect(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])

    m = fpgaMajVer(bus,i.igloo["fpgaMajVer"]["register"], 1)
    print m.run()
    m = fpgaMinVer(bus,i.igloo["fpgaMinVer"]["register"], 1)
    print m.run()
    m = ones(bus,i.igloo["ones"]["register"], 1)
    print m.run()
    m = zeroes(bus,i.igloo["zeroes"]["register"], 1)
    print m.run()
    m = fpgaTopOrBottom(bus,i.igloo["fpgaTopOrBottom"]["register"], 1)
    print m.run()
    m = uniqueID(bus,i.igloo["uniqueID"]["register"], 1)
    print m.run()
    m = statusReg(bus,i.igloo["statusReg"]["register"], 1)
    print m.run()
    m = cntrRegDisplay(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()
    m = clk_count(bus,i.igloo["clk_count"]["register"], 1)
    print m.run()
    m = rst_QIE_count(bus,i.igloo["rst_QIE_count"]["register"], 1)
    print m.run()
    m = wte_count(bus,i.igloo["wte_count"]["register"], 1)
    print m.run()
    m = capIDErr_count(bus,i.igloo["capIDErr_count"]["register"], 1)
    print m.run()
    # m = inputSpy(bus,i.igloo["inputSpy"]["register"], 1)
    # print m.run()
    # m = inputSpy_512Reads(bus,i.igloo["inputSpy"]["register"], 1)
    # print m.run()
    m = CI_Mode_On(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()
    m = CI_Mode_Off(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()
    # m = spy96Bits(bus,i.igloo["spy96Bits"]["register"], 1)
    # print m.run()
    # m = scratchReg(bus,i.igloo["scratchReg"]["register"], 1)
    # print m.run()

def readOutInputSpy(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])
    m = cntrRegDisplay(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()
    m = cntrRegChange(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run('WrEn_InputSpy', '1')

    m = inputSpy(bus,i.igloo["inputSpy"]["register"], 512)
    print m.run()

def processInputSpy(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])
    m = inputSpy_512Reads(bus,i.igloo["inputSpy"]["register"], 1)
    print m.run()

def cntrRegShowAll(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])
    m = cntrRegDisplay(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()

def setCI_mode(slot, bus, onOffBit):
    def openIgloo(slot):
        q.openChannel()
        #the igloo is value "3" in I2C_SELECT table
        bus.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        bus.sendBatch()
    openIgloo(0)

    if onOffBit == 1:
        m = CI_Mode_On(bus,i.igloo["cntrReg"]["register"], 1)
        print m.run()

    elif onOffBit == 0:
        m = CI_Mode_Off(bus,i.igloo["cntrReg"]["register"], 1)
        print m.run()

    else: print 'Invalid onOffBit'

def readBridgeIglooReg(bus):
    h.openChannel(slot,bus)
    bus.write(0x00,[0x06])
    bus.write(h.getCardAddress(slot),[0x22])
    bus.read(h.getCardAddress(slot),4)
    read1 = bus.sendBatch()[-1]
    print 'BRIDGE IGLOO REG Read: '+str(read1)

def writeBridgeIglooReg(bus):
    h.openChannel(slot,bus)
    bus.write(0x00,[0x06])
    bus.write(h.getCardAddress(slot),[0x22,0xe7,0x07,0,0])
    write2 = bus.sendBatch()[0]
    print 'BRIDGE IGLOO REG Write: '+str(write2)

def turnOnCI(bus):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])
    m = CI_Mode_On(bus,i.igloo["cntrReg"]["register"], 1)
    print m.run()

def displayCI(bus,slot):
    h.openChannel(slot,bus)
    bus.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])
    m = CI_Mode_Display(bus,i.igloo["cntrReg"]["register"], 1)
    m.run()

###########################################
# RUN FUNCTIONS
###########################################

if __name__ == '__main__':
    #runAll()
    # runSelect()
    #readOutInputSpy()
    processInputSpy()
    #setCI_MODE(1)
    # readBridgeIglooReg()
    # writeBridgeIglooReg()
    # readBridgeIglooReg()
    #turnOnCI()
    #displayCI(slot)
