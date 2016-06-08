#/usr/bin/python
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

# 1. Determine address (eg. Fanout is 0x72 unless switches are flipped).
def find_address(init_add):
    byte = SR(init_add)
    while byte == None and init_add <= 0xa0:
        init_add += 1
        byte = SR(init_add)
    return init_add

# 2. Determine byte to set on Fanout to open i2c with ngCCM U10 (0x74). Verify address of U10.
def determine_byte(add_1, add_2):
    byte_1 = 1
    SW(add_1,byte_1)
    byte_2 = SR(add_2)
    while byte_2 == None and byte_1 <= 0x80:
        byte_1 *= 2
        SW(add_1,byte_1)
        byte_2 = SR(add_2)
    return byte_1

# 3. Determine

################################################################################
# Test - the test() function is executed by the client
################################################################################

def test():
    fan = 0x72
    u10 = 0x74
    print '\n### Write 0x00 to Fanout for initiation!'
    SW(fan,0x00)
    print '\n### Find address and determine byte for Fanout.'
    fan_add = find_address(0x70)
    print '\n'
    fan_byte = determine_byte(fan_add,u10)
    print '\n### Find address and determine byte for ngCCM U10.'
    u10_add = find_address(0x73)
    print '\n'
    u10_byte = SR(u10_add)
    print 'fan add: ', hex(fan_add)
    print 'fan byte: ', hex(fan_byte)
    print 'u10 add: ', hex(u10_add)
    print 'u10 byte: ', hex(u10_byte)

################################################################################
