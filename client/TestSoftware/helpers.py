#helpers.py
##Helper functions for tests:
def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))
def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret
def getByteFromBits(bitList):
    return int(''.join(str(i) for i in bitList), 2)
def getBytesFromBits(bitList):
    ret = []
    for i in xrange(len(bitList)/8):
        ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
    return ret
def readBinaryRegister(bus, address, register, numBytes):
    return getBitsFromBytes(readFromRegister(bus, address, register, numBytes))
def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[1].split():
        ret.append(int(i))
    ret=ret[1:]
    return ret
def writeToRegister(bus, address, register, bytesToWrite):
    bus.write(address, [register] + list(bytesToWrite))
    return None
def toHex(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    s = ""
    return '0x' + s.join(message_list)

def reverseBytes(message):
    message_list = message.split()
    message_list.reverse()
    s = " "
    return s.join(message_list)
