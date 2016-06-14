testList = []

##Helper functions for tests:
def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))

def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret

def getByteFromBits(bitList):
    return int(''.join(bitList), 2)
def getBytesFromBits(bitList):
    ret = []
    for i in xrange(len(bitList)/8):
        ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
    return ret

def readFromRegister(bus, address, register, numBytes):
    bus.write(address, [register])
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[1].split():
        ret.append(int(i))
    return ret
def writeToRegister(bus, address, register, bytesToWrite):
    bus.write(address, [register] + list(bytesToWrite))
    return None


def test1(iterations, address):
    return (passes, fails)
