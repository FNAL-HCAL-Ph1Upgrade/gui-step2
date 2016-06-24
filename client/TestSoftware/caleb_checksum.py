# It is time to check your sum!
# CRC = Cyclic Redundancy Check

import collections

# Convert string of ints to list of ints.
def toIntList(message, base=10):
    mList = message.split()
    for byte in xrange(len(mList)):
        mList[byte] = int(mList[byte], base)
    return mList

# Check Sum function from Temp/Humi Documentation.
def checkCRC(message, numBytes, base=10, verbose=0):
    POLYNOMIAL = 0x131 # x^8 + x^5 + x^4 + 1 -> 9'b100110001 = 0x131
    crc = 0
    mList = toIntList(message, base)
    errorCode = mList[0]
    dataList = mList[1:-1]
    checksum = mList[-1]
    if verbose > 2:
        print 'data = ',dataList
        print 'checksum = ',checksum
    if errorCode != 0:
        return 'I2C_BUS_ERROR'
    # calculates 8-bit checksum with give polynomial
    for byteCtr in xrange(numBytes):
        crc ^= dataList[byteCtr]
        # crc &= 0xFF
        if verbose > 1:
            print "CRC = ",crc
        for bit in xrange(8,0,-1):
            if crc & 0x80: # True if crc >= 128, False if crc < 128
                crc = (crc << 1) ^ POLYNOMIAL
                # crc &= 0xFF
                if verbose > 1:
                    print 'true crc = ',crc
            else: # crc < 128
                crc = (crc << 1)
                # crc &= 0xFF
                if verbose > 1:
                    print 'false crc = ',crc
    if verbose > 0:
        print 'CRC = ',crc
        print 'checksum = ',checksum
    if crc != checksum:
        return 'CHECKSUM_ERROR'
    return 'CHECKSUM_OK'

# Two Binary Data Bytes
binaryData = '01110000 00111100'
# One Binary Checksum Byte
binaryChecksum = '10000011'

# message = 'errorCode byte1 byte2 checksum'

# Happy Data has a valid checksum! :)
binDataHappy = '0 01110000 00111100 10000011'
intDataHappy = '0 112 60 131'
# value = 28732

# Sad Data has an invalid checksum. :(
binDataSad = '0 01110000 00111100 10000010'
intDataSad = '0 112 60 130'

# An I2S Bus Error is seen by a nonzero first bit (1).
binI2Cerror = '1 01110000 00111100 10000011'
intI2Cerror = '1 112 60 131'

# makes some lists to iterate through 3 tests
testList = ['Happy Data', 'Sad Data', 'I2C Error']
binDataList = [binDataHappy, binDataSad, binI2Cerror]
intDataList = [intDataHappy, intDataSad, intI2Cerror]

def tempTest(numTests):
    for test in xrange(numTests):
        print '\n',testList[test]
        print binDataList[test], ' : ', checkCRC(binDataList[test], 2, 2)
        print intDataList[test], ' : ', checkCRC(intDataList[test], 2, 10),'\n'

def uniqueIDTest(idList):
    for ID in idList:
        message = ID
        print '\n--- Raw ID: ',ID
        print '*** New ID: ',message
        print checkCRC(message,7,10,2)

idList = [
    '0 112 138 191 234 0 0 0 132',
    '0 112 54 183 234 0 0 0 192',
    '0 112 236 157 234 0 0 0 142',
    '0 112 96 185 234 0 0 0 254',
    '0 112 121 170 215 0 0 0 212'
]

# uniqueIDTest([idList[0]])

