import sys
sys.path.append('../')
from client import webBus
from operator import add
import TestLib as t
import QIELib as q
b = webBus("pi5")

# Examlpe for register address 0x00
def bridge0(rm,slot):
    t.openRM(rm)
    b.write(q.QIEi2c[slot],[0x00])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]

# Bridge Register Tests

def runBridgeTests(RMList, num_slots, num_tests, verbosity=0):
    print '\n\nBRIDGE TEST\n\n'
    total_passed = 0
    total_failed = 0
    total_neither = 0
    total_number_tests = num_slots * num_tests
    total_test_list = [total_passed, total_failed, total_neither]
    for rm in RMList:
        t.openRM(rm)
        print '\n-------------------- Test RM: '+str(rm)+' --------------------'
        for slot in xrange(num_slots):
            b.write(0x00,[0x06])
            print '\n-------------------- Test Slot: '+str(slot)+' --------------------'
            test_list = bridgeTests(slot,num_tests)
            total_test_list = map(add, total_test_list, test_list)
            daisyChain = q.qCard(webBus("pi5",0), q.QIEi2c[slot])
            print '\n~~~~~~~~~~ QIE Daisy Chain ~~~~~~~~~~'
            print str(daisyChain)
            if verbosity:
                print '\nNumber passed = '+str(test_list[0])
                print 'Number failed = '+str(test_list[1])
                print 'Number neither pass nor fail = '+str(test_list[2])+'\n'

    # Print Final Test Results for Bridge FPGA
    print '\n\n########   Final Test Results  ########\n'
    print 'Total Number of Tests = '+str(total_number_tests)
    print 'Number passed = '+str(total_test_list[0])
    print 'Number failed = '+str(total_test_list[1])
    print 'Number neither pass nor fail = '+str(total_test_list[2])
    print 'Check total number of tests: '+str(total_number_tests == sum(total_test_list))+'\n'

def bridgeTests(slot, num_tests, verbosity=0):
    passed = 0
    failed = 0
    neither = 0
    print '## Number of Tests: '+str(num_tests)
    for test in xrange(num_tests):
        print '\n### Bridge Test: '+str(test)+' ###'
        print '\n### Test Name: '+str(bridgeDict[test]['name'])
        function = bridgeDict[test]['function']
        address = bridgeDict[test]['address']
        num_bytes = bridgeDict[test]['bits']/8
        message = t.readRegisterBridge(slot, address, num_bytes)
        print '\n*********** RAW MESSAGE :'+str(t.reverseBytes(message))+'\n'
        result = function(message)
        if result == 'PASS':
            passed += 1
        elif result == 'FAIL':
            failed += 1
        else:
            print 'Neither PASS Nor FAIL'
            neither += 1
        if verbosity:
            print 'Register Name: '+str(bridgeDict[test]['name'])
            print 'Register Value: '+str(message)
            print 'Test Result: '+str(result)

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
    print 'correct value: '+str(correct_value)
    print 'ASCII message: '+str(message)
    return passFail(message==correct_value)

def idStringCont(message):
    correct_value = "Brdg"
    message = t.toASCII(message)
    print 'correct value: '+str(correct_value)
    print 'ASCII message: '+str(message)
    return passFail(message==correct_value)

def fwVersion(message):
    # correct_value = "N/A" # We need to find Firmware Version
    message = t.toHex(message)
    # print 'correct value: '+str(correct_value)
    print 'hex message: '+str(message)
    return message

def ones(message):
    correct_value = '0xffffffff'
    hex_message = t.toHex(message,0)
    print 'correct value: '+str(correct_value)
    print 'int message: '+str(message)
    print 'hex message: '+str(hex_message)
    return passFail(hex_message==correct_value)

def zeroes(message):
    correct_value = '0x00000000'
    hex_message = t.toHex(message,0)
    print 'correct value: '+str(correct_value)
    print 'int message: '+str(message)
    print 'hex message: '+str(hex_message)
    return passFail(hex_message==correct_value)

def onesZeroes(message):
    correct_value = '0xaaaaaaaa'
    hex_message = t.toHex(message,0)
    print 'correct value: '+str(correct_value)
    print 'int message: '+str(message)
    print 'hex message: '+str(hex_message)
    return passFail(hex_message==correct_value)

def qieDaisyChain0(message):
    hex_message = t.toHex(message,1)
    print 'int message: '+str(message)
    print 'hex message:'+str(hex_message)
    split_message = t.splitMessage(hex_message,6)
    for i in xrange(len(split_message)):
        print 'QIE '+str(i+1)+': '+str(split_message[i])
    return hex_message

def qieDaisyChain1(message):
    hex_message = t.toHex(message,1)
    print 'int message: '+str(message)
    print 'hex message:'+str(hex_message)
    split_message = t.splitMessage(hex_message,6)
    for i in xrange(len(split_message)):
        print 'QIE '+str(i+7)+': '+str(split_message[i])
    return hex_message

    return hex_message

def simplePrint(message):
    hex_message = t.toHex(message,1)
    print 'int message: '+str(message)
    print 'hex message:'+str(hex_message)
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
        'bits' : 11,
        'write' : True
    },
    16 : {
        'name' : 'ControlReg',
        # 'function' : controlReg,
        'function' : simplePrint,
        'address' : 0x2A,
        'bits' : 32,
        'write' : True
    },
    17 : {
        'name' : 'orbit_histo[167:144]',
        # 'function' : orbitHisto6,
        'function' : simplePrint,
        'address' : 0x2B,
        'bits' : 24,
        'write' : False
    },
    18 : {
        'name' : 'orbit_histo[143:120]',
        # 'function' : orbitHisto5,
        'function' : simplePrint,
        'address' : 0x2C,
        'bits' : 24,
        'write' : False
    },
    19 : {
        'name' : 'orbit_histo[119:96]',
        # 'function' : orbitHisto4,
        'function' : simplePrint,
        'address' : 0x2D,
        'bits' : 24,
        'write' : False
    },
    20 : {
        'name' : 'orbit_histo[95:72]',
        # 'function' : orbitHisto3,
        'function' : simplePrint,
        'address' : 0x2E,
        'bits' : 24,
        'write' : False
    },
    21 : {
        'name' : 'orbit_histo[71:48]',
        # 'function' : orbitHisto2,
        'function' : simplePrint,
        'address' : 0x2F,
        'bits' : 24,
        'write' : False
    },
    22 : {
        'name' : 'orbit_histo[47:24]',
        # 'function' : orbitHisto1,
        'function' : simplePrint,
        'address' : 0x30,
        'bits' : 24,
        'write' : False
    },
    23 : {
        'name' : 'orbit_histo[23:0]',
        # 'function' : orbitHisto0,
        'function' : simplePrint,
        'address' : 0x31,
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

# runBridgeTests(RMList, num_slots, num_tests, verbosity=0)
# 27 is max num of tests
runBridgeTests([0],4,27,0)
