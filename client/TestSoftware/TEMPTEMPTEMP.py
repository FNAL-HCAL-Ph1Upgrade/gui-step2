from client import webBus
from operator import add
import TestLib as t
import time
b = webBus("pi6",0)

# Cryptic 0x70 Reset
def reset(ngccm):
    b.write(0x72,[ngccm])
    b.write(0x74,[0x08])
    b.write(0x70,[0x3,0])
    b.write(0x70,[0x1,0])
    return b.sendBatch()

# Read from Bridge
def readBridge(slot, address, num_bytes):
    b.write(t.bridgeAddress(slot),[address])
    b.read(t.bridgeAddress(slot), num_bytes)
    message = b.sendBatch()[-1]
    return t.reverseBytes(message)

# Write to Bridge
def writeBridge(rm,slot,address,messageList):
    t.openRM(b,rm)
    b.write(t.bridgeAddress(slot),[address] + messageList)
    return b.sendBatch()

# Bridge Register Tests

def runBridgeTests(RMList, slotList, testList, verbosity=0):
    print '\n\nBRIDGE TEST\n\n'
    total_passed = 0
    total_failed = 0
    total_neither = 0
    num_slots = 0
    for rm in RMList:
        num_slots += len(slotList[4-rm])
    num_tests = len(testList)
    total_number_tests = num_slots * num_tests
    total_test_list = [total_passed, total_failed, total_neither]
    for rm in RMList:
        t.openRM(b,rm)
        print '\n-------------------- Test RM: ', rm, ' --------------------'
        for slot in slotList[4-rm]:
            b.write(0x00,[0x06])
            print '\n-------------------- Test Slot: ', slot, ' --------------------'
            test_list = bridgeTests(slot,testList, verbosity)
            total_test_list = map(add, total_test_list, test_list)
            # daisyChain = q.qCard(webBus("pi5",0), t.bridgeAddress(slot))
            # print '\n~~~~~~~~~~ QIE Daisy Chain ~~~~~~~~~~'
            # print str(daisyChain)
            if verbosity:
                print '\nNumber passed = ', test_list[0]
                print 'Number failed = ', test_list[1]
                print 'Number neither pass nor fail = ', test_list[2], '\n'

    # Print Final Test Results for Bridge FPGA
    print '\n\n########   Final Test Results  ########\n'
    print 'Total Number of Tests = ', total_number_tests
    print 'Number passed = ', total_test_list[0]
    print 'Number failed = ', total_test_list[1]
    print 'Number neither pass nor fail = ', total_test_list[2]
    print 'Check total number of tests: ', total_number_tests == sum(total_test_list), '\n'

def bridgeTests(slot, testList, verbosity=0):
    passed = 0
    failed = 0
    neither = 0
    num_tests = len(testList)
    print '## Number of Tests: ', num_tests
    for test in testList:
        print '\n### Bridge Test: ', test, ' ###'
        print '### Test Name: ', bridgeDict[test]['name']
        function = bridgeDict[test]['function']
        address = bridgeDict[test]['address']
        num_bytes = bridgeDict[test]['bits']/8
        message = readBridge(slot, address, num_bytes)
        print '*** RAW MESSAGE :', t.reverseBytes(message)

        # Check for i2c Error
        mList = message.split()
        error = mList.pop(0)
        if int(error) != 0:
            print '\n@@@@@@ I2C ERROR : ',message,'\n'
        message = " ".join(mList)

        result = function(message)
        print 'RESULT = ',result
        if result == 'PASS':
            passed += 1
        elif result == 'FAIL':
            failed += 1
        else:
            print 'Neither PASS Nor FAIL'
            neither += 1
        if verbosity:
            print 'Register Name: ', bridgeDict[test]['name']
            print 'Register Value: ', message
            print 'Test Result: ', result

    test_list = [passed, failed, neither]
    return test_list


##### TestLib ########

def passFail(result):
    if result:
        return 'PASS'
    return 'FAIL'

def idString(message):
    correct_value = "HERM"
    message = t.toASCII(message)
    print 'correct value: ', correct_value
    print 'ASCII message: ', message
    return passFail(message==correct_value)

def idStringCont(message):
    correct_value = "Brdg"
    message = t.toASCII(message)
    print 'correct value: ', correct_value
    print 'ASCII message: ', message
    return passFail(message==correct_value)

def fwVersion(message):
    # correct_value = "N/A" # We need to find Firmware Version
    message = t.toHex(message)
    # print 'correct value: ', correct_value
    print 'hex message: ', message
    return message

def ones(message):
    correct_value = '0xffffffff'
    hex_message = t.toHex(message,0)
    print 'correct value: ', correct_value
    print 'int message: ', message
    print 'hex message: ', hex_message
    return passFail(hex_message==correct_value)

def zeroes(message):
    correct_value = '0x00000000'
    hex_message = t.toHex(message,0)
    print 'correct value: ', correct_value
    print 'int message: ', message
    print 'hex message: ', hex_message
    return passFail(hex_message==correct_value)

def onesZeroes(message):
    correct_value = '0xaaaaaaaa'
    hex_message = t.toHex(message,0)
    print 'correct value: ', correct_value
    print 'int message: ', message
    print 'hex message: ', hex_message
    return passFail(hex_message==correct_value)

def orbitHisto(message):
    simplePrint(message)
    value = t.getValue(message)
    return value

def qieDaisyChain0(message):
    hex_message = t.toHex(message,1)
    print 'int message: ', message
    print 'hex message:', hex_message
    split_message = t.splitMessage(hex_message,6)
    for i in xrange(len(split_message)):
        print 'QIE ',i+1,': ',split_message[i]
    return hex_message

def qieDaisyChain1(message):
    hex_message = t.toHex(message,1)
    print 'int message: ', message
    print 'hex message:', hex_message
    split_message = t.splitMessage(hex_message,6)
    for i in xrange(len(split_message)):
        print 'QIE ',i+7,': ',split_message[i]
    return hex_message

    return hex_message

def simplePrint(message):
    hex_message = t.toHex(message,1)
    print 'int message: ', message
    print 'hex message:', hex_message
    return hex_message

# Input and compare all correct values in same format...

bridgeDict = {
    0 : {
        'name' : 'ID string',
        'function' : idString,
        'address' : 0x00,
        'bits' : 32,
        'write' : False
    },
    1 : {
        'name' : 'ID string cont',
        'function' : idStringCont,
        'address' : 0x01,
        'bits' : 32,
        'write' : False
    },
    2 : {
        'name' : 'FW Version',
        'function' : fwVersion,
        'address' : 0x04,
        'bits' : 32,
        'write' : False
    },
    3 : {
        'name' : 'Ones',
        'function' : ones,
        'address' : 0x08,
        'bits' : 32,
        'write' : False
    },
    4 : {
        'name' : 'Zeroes',
        'function' : zeroes,
        'address' : 0x09,
        'bits' : 32,
        'write' : False
    },
    5 : {
        'name' : 'OnesZeroes',
        'function' : onesZeroes,
        'address' : 0x0A,
        'bits' : 32,
        'write' : False
    },
    6 : {
        'name' : 'Scratch',
        # 'function' : scratch,
        'function' : simplePrint,
        'address' : 0x0B,
        'bits' : 32,
        'write' : True
    },
    7 : {
        'name' : 'Status',
        # 'function' : status,
        'function' : simplePrint,
        'address' : 0x10,
        'bits' : 32,
        'write' : False
    },
    8 : {
        'name' : 'I2C_SELECT',
        # 'function' : i2cSelect,
        'function' : simplePrint,
        'address' : 0x11,
        'bits' : 32, # 8 bits in documentation
        'write' : True
    },
    9 : {
        'name' : 'Clock Counter',
        # 'function' : clockCounter,
        'function' : simplePrint,
        'address' : 0x12,
        'bits' : 32,
        'write' : False
    },
    10 : {
        'name' : 'RES_QIE Counter',
        # 'function' : resQieCounter,
        'function' : simplePrint,
        'address' : 0x13,
        'bits' : 32,
        'write' : False
    },
    11 : {
        'name' : 'WTE Counter',
        # 'function' : wteCounter,
        'function' : simplePrint,
        'address' : 0x14,
        'bits' : 32,
        'write' : False
    },
    12 : {
        'name' : 'BkPln_Spare_1 Counter',
        # 'function' : bkPlnCounter1,
        'function' : simplePrint,
        'address' : 0x15,
        'bits' : 32,
        'write' : False
    },
    13 : {
        'name' : 'BkPln_Spare_2 Counter',
        # 'function' : bkPlnCounter2,
        'function' : simplePrint,
        'address' : 0x16,
        'bits' : 32,
        'write' : False
    },
    14 : {
        'name' : 'BkPln_Spare_3 Counter',
        # 'function' : bkPlnCounter3,
        'function' : simplePrint,
        'address' : 0x17,
        'bits' : 32,
        'write' : False
    },
    15 : {
        'name' : 'igloo2 FPGA Control',
        # 'function' : iglooControl,
        'function' : simplePrint,
        'address' : 0x22,
        'bits' : 16, # 11
        'write' : True
    },
    16 : {
        'name' : 'ControlReg',
        # 'function' : controlReg,
        'function' : simplePrint,
        'address' : 0x18,
        'bits' : 32,
        'write' : True
    },
    17 : {
        'name' : 'orbit_histo[167:144]',
        'function' : orbitHisto,
        'address' : 0x19,
        'bits' : 24,
        'write' : False
    },
    18 : {
        'name' : 'orbit_histo[143:120]',
        'function' : orbitHisto,
        'address' : 0x1A,
        'bits' : 24,
        'write' : False
    },
    19 : {
        'name' : 'orbit_histo[119:96]',
        'function' : orbitHisto,
        'address' : 0x1B,
        'bits' : 24,
        'write' : False
    },
    20 : {
        'name' : 'orbit_histo[95:72]',
        'function' : orbitHisto,
        'address' : 0x1C,
        'bits' : 24,
        'write' : False
    },
    21 : {
        'name' : 'orbit_histo[71:48]',
        'function' : orbitHisto,
        'address' : 0x1D,
        'bits' : 24,
        'write' : False
    },
    22 : {
        'name' : 'orbit_histo[47:24]',
        'function' : orbitHisto,
        'address' : 0x1E,
        'bits' : 24,
        'write' : False
    },
    23 : {
        'name' : 'orbit_histo[23:0]',
        'function' : orbitHisto,
        'address' : 0x1F,
        'bits' : 24,
        'write' : False
    },

    # QIE Daisy Chains. Chains 2 and 3 are not used.
    # Conflict between Orbits 0, 1 and Daisy Chains 0, 1.
    # Addresses 0x30, 0x31.
    24 : {
        'name' : 'QIE Daisy Chain 0',
        'function' : qieDaisyChain0,
        # 'function' : simplePrint,
        'address' : 0x30,
        # 'address' : 0x32,
        'bits' : 384,
        'write' : True
    },
    25 : {
        'name' : 'QIE Daisy Chain 1',
        'function' : qieDaisyChain1,
        # 'function' : simplePrint,
        'address' : 0x31,
        # 'address' : 0x33,
        'bits' : 384,
        'write' : True
    },
    26 : {
        'name' : 'Thermometer One Wire',
        # 'function' : thermOneWire,
        'function' : simplePrint,
        'address' : 0x40,
        'bits' : 32, # TBD in documentation
        'write' : True
    },
}

# I2C_SELECT Table (address 0x11)
i2cDict = {
    0 : {
        'name' : 'no select',
        # 'function' : noSelect,
        'function' : simplePrint,
        'value' : 0x00
    },
    1 : {
        'name' : 'VTTX 1 (Twin Transmitter)',
        # 'function' : vttx1,
        'function' : simplePrint,
        'value' : 0x01,
        'address' : 0x7E
    },
    2 : {
        'name' : 'VTTX 2 (Twin Transmitter)',
        # 'function' : vttx2,
        'function' : simplePrint,
        'value' : 0x02,
        'address' : 0x7E
    },
    3 : {
        'name' : 'igloo2 FPGA (unique FPGA for HE, Top for HB)',
        # 'function' : vttx1,
        'function' : simplePrint,
        'value' : 0x03,
        'address' : 0x09
    },
    4 : {
        'name' : 'DS28CM00 Silicon Serial Number (Unique ID)',
        # 'function' : uniqueID,
        'function' : simplePrint,
        'value' : 0x04,
        'address' : 0x50
    },
    5 : {
        'name' : 'SHT21 Humidity and Temperature Sensor',
        # 'function' : temp,
        'function' : simplePrint,
        'value' : 0x05,
        'address' : 0x40
    }
    # igloo2 Bot_FPGA does not exist for HE (only for HF)!
}

###############################################################################

# runBridgeTests(RMList, slotList, testList, verbosity=0)
# 27 is max num of tests

def control_reg_orbit_histo(rm,slot,delay):
    writeBridge(rm,slot,0x18,[2,0,0,0])
    writeBridge(rm,slot,0x18,[1,0,0,0])
    time.sleep(delay)
    writeBridge(rm,slot,0x18,[0,0,0,0])
    # runBridgeTests([rm],t.getSlotList(rm,slot),range(16,24),0)
    t.openRM(b,rm)
    message = readBridge(slot, 0x1D, 3)
    value = t.getValue(message)
    return value

# writeBridge(2,3,0x22,[0xE0,4])
# writeBridge(2,4,0x22,[0xE0,4])
# writeBridge(1,1,0x22,[0xE0,4])
# writeBridge(1,4,0x22,[0xE0,4,0,0])

# print reset(1)
# print reset(2)

# runBridgeTests([4], [[1,4],0,0,0], [15])
# runBridgeTests([2,1], [0,0,[1,4],[1]], range(16,24))

# control_reg_orbit_histo(1,1,0)
# control_reg_orbit_histo(1,1,1)

