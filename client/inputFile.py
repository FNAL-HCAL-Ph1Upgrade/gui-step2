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


################################################################################
# Test - the test() function is executed by the client
################################################################################

def test():
    print 'return: ', SR(0x72)
    print 'return: ', SRs(0x72)
    # SW(0x72,0x01)
    # SR(0x74)
    # SIMPLE_CHECK_WRITE(0x72, 0x01)
    # SIMPLE_CHECK_WRITE(0x72, 0x02)
################################################################################
