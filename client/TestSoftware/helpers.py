#helpers.py
##Helper functions for tests:
def getBitsFromByte(decimal):
    a = list('%08d' % int(bin(decimal)[2:]))
    a.reverse()
    return a

def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret

def getByteFromBits(bitList):
    bitList.reverse()
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
    bus.sleep(1000)
    bus.read(address, numBytes)
    ret = []
    for i in bus.sendBatch()[2].split():
        ret.append(int(i))
    ret = ret[1:]
    return ret

def writeToRegister(bus, address, register, bytesToWrite):
    bus.write(address, [register] + list(bytesToWrite))
    return None

def toHex(message,option=0):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = hex(int(message_list[byte]))
        message_list[byte] = message_list[byte][2:]
        if len(message_list[byte]) == 1:
            message_list[byte] = '0' + message_list[byte]
    if option == 2:
        s = ":"
        return s.join(message_list)
    if option == 1:
        s = " "
        return s.join(message_list)
    s = ""
    return '0x' + s.join(message_list)

def getValue(message):
    hex_message = toHex(message)[2:]
    return int(hex_message,16)

def getMessageList(value,num_bytes):
    hex_message = hex(value)[2:]
    length = len(hex_message)
    zeros = "".join(list('0' for i in xrange(8-length)))
    hex_message = zeros + hex_message
    # print 'hex message = '+str(hex_message)
    mList = list(int(hex_message[a:a+2],16) for a in xrange(0,2*num_bytes,2))
    mList.reverse()
    return mList

def reverseBytes(message):
    message_list = message.split()
    message_list.reverse()
    s = " "
    return s.join(message_list)

# Parse Serial Number (6 bytes) from 8 byte Registration Number.
def serialNum(message):
    message_list = message.split()
    message_list = message_list[2:-1]
    s = " "
    return s.join(message_list)

def sensorTemp(slot,b):
    b.write(slot,[0x11,0x05,0,0,0])

    # q.openChannel(rm,slot)
    # b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,3)

    data = ((b.sendBatch()[2]).split())[1:]
    checksum = data[2] # 3rd byte of data is the checksum
    print 'Checksum: ' + hex(int(checksum))[2:]

    # Splitting the incoming data & concatenating strings of binary bytes
    data = format(int(data[0]),'08b') + format(int(data[1]),'08b')
    print '2 data bytes: ' + data
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting temp using equation
    temp = (-46.85) +175.72*(data)/(2**16)
    return temp


def sensorHumid(slot,b):
    # q.openChannel(rm,slot)
    # b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x00,[0x06])
    b.sendBatch()

    b.write(slot,[0x11,0x05,0,0,0])
    b.write(0x40,[0xf5])
    b.read(0x40,2)

    data = b.sendBatch()[2]
  #  data = b.sendBatch()[2]
    # Splitting the incoming data & concatenating strings of binary bytes
    # using [1] and [2] to skip over the error byte
    data = format(int(data.split()[1]),'08b') + format(int(data.split()[2]),'08b')
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting humidity using equation
    humid = (-6.0) + 125.0 * (data)/(2**16)
    return humid
