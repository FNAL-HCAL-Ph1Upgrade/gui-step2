#!/usr/bin/python
#
#inputFile.py
#a test input file for the client
################################################################################
# imports - must have in all files using these commands
################################################################################
from client import SR, SW, CR, CW, SRs, CRs
################################################################################

################################################################################
# test-specific functions - defined by tester
################################################################################
def SIMPLE_CHECK_WRITE(address, value):
    SR(address) #for reference
    SW(address, value)
    if SR(address) == value:
        return True
    else:
        return False

def COMPLEX_CHECK_WRITE(address, register, value):
    CR(address, register) #for reference
    CW(address, register, value)
    if CR(address, register) == value:
        return True
    else:
        return False
################################################################################
# 0. Initial Test
def initial_test():
    print SR(0x71) == None
    print SRs(0x71) == None
    # SW(0x72,0x01)
    # SR(0x74)
    # SIMPLE_CHECK_WRITE(0x72, 0x01)
    # SIMPLE_CHECK_WRITE(0x72, 0x02)

# 1. Determine address of Fanout (0x72 unless switches are flipped).
def find_fan(init_add):
    byte = SR(init_add)
    while byte == None and init_add < 0xa0:
        init_add += 1
        byte = SR(init_add)
    return init_add

# 2. Determine bits to set on Fanout to open i2c with ngCCM FPGA Bridge (0x74). Verify address of Fanout.

# 3. Determine

################################################################################
# Test - the test() function is executed by the client
################################################################################

def test():
    fan_add = find_fan(0x75)
    fan_byte = SR(fan_add)
    print 'fan add: ', hex(fan_add)
    print 'fan byte: ', hex(fan_byte)

################################################################################
