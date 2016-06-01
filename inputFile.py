#inputFile.py
#a test input file for the client

#write thing to address and check if read of address is same thing

from client import SR, SW, CR, CW, SRs, CRs

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

def test():
    print SR(0x72)
    SIMPLE_CHECK_WRITE(0x72, 0x01)
    print SR(0x72)
    SIMPLE_CHECK_WRITE(0x72, 0x03)
