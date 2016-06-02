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
    SRs(address) #for reference
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

#this is a comment

def test():
    print "\n\nWriting to 0x01 on Fanout:"
    SIMPLE_CHECK_WRITE(0x72, 0x01)
    print "\n\nWriting 0xff on nGCCM:"
    SIMPLE_CHECK_WRITE(0x74, 0xff)
    print "\n\nWriting to 0x02 on Fanout:"
    SIMPLE_CHECK_WRITE(0x72, 0x02)
    print "\n\nWriting 0x01 on nGCCM:"
    SIMPLE_CHECK_WRITE(0x74, 0x01)
    print "\n\nWriting to 0x01 on Fanout:"
    SIMPLE_CHECK_WRITE(0x72, 0x01)
    print "\n\nWriting 0xaa on nGCCM:"
    SIMPLE_CHECK_WRITE(0x74, 0xaa)
################################################################################
