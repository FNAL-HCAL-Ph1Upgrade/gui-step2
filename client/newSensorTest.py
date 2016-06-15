from client import webBus
import QIELib
b = webBus("pi5",0)
q = QIELib

# It is time to check your sum!
# CRC = Cyclic Redundancy Check

# Convert string of ints to list of ints.
def toIntList(message):
    message_list = message.split()
    for byte in xrange(len(message_list)):
        message_list[byte] = int(message_list[byte],2)
    return message_list

def checkCRC(data, numBytes, checksum):
    POLYNOMIAL = 0x131 # x^8 + x^5 + x^4 + 1 -> 9'b100110001 = 0x131
    crc = 0
    dataList = toIntList(data)
    # calculates 8-bit checksum with give polynomial
    for byteCtr in xrange(numBytes):
        crc ^= dataList[byteCtr]
        for bit in xrange(8,0,-1):
            if crc & 0x80:
                crc = (crc << 1) ^ POLYNOMIAL
            else:
                crc = (crc << 1)
    if crc != checksum:
        return 'CHECKSUM_ER'
    return 'CHECKSUM_OK'

#returns the temperature of the QIE card
def sensorTemp(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,3)

    data = b.sendBatch()[2]
    checksum = int(data[2]) # 3rd byte of data is the checksum

    print "                           " + checkCRC(data, 2, checksum)

    # Splitting the incoming data & concatenating strings of binary bytes
    data = format(int(data.split()[0]),'08b') + format(int(data.split()[1]),'08b')
    print "2 data bytes: " + data
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting temp using equation
    temp = (-46.85) +175.72*(data)/(2**16)

    print "                             Temp: %.2f" %temp
    
    return temp

print "%.2f" %(sensorTemp(0,2))

# #returns the temperature of the QIE card
# def sensorTemp(rm,slot):
#     q.openChannel(rm,slot)
#     b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
#     b.write(0x40,[0xf3])
#     b.read(0x40,2)
#
#     data = b.sendBatch()[2]
#     #Splitting the incoming data and reversing the order of bytes
#     #(the read function's inherent reversal of bytes isn't compatible with
#     #this particular sensor's desired output order)
#
#     data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
#     #Converting the temperature using equation
#     temp = (-46.85) +175.72*(data)/(2**16)
#
#     return temp
#
# print "%.2f" %(sensorTemp(0,2))


#returns the relative humidity of the QIE card
def sensorHumid(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf5])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    #Splitting the incoming data and reversing the order of bytes
    #(the read function's inherent reversal of bytes isn't compatible with
    #this particular sensor's desired output order)

    data = format(int(data.split()[0]),'08b') + format(int(data.split()[1]),'08b')
    data = int(data[0:14] + "00") # zero-ing out the 2 status bits

    humid = -6.0 + 125.0*(data)/(2**16)

    return humid

'''
    byte1 = format(int(data.split()[0]),'08b')
    byte2 = format(int(data.split()[1]),'08b')
    print "humid byte1+byte2 = " + byte1 + "+" + byte2
    catBytes = byte1+byte2
    print "catBytes = " + catBytes
    useTheseBytes = catBytes[0:14] + "00"
    print "useThese = " + useTheseBytes

    newData = int(useTheseBytes,2)

    oldData = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
    #Converting the humidity using equation
    newHumid = -6.0 + 125.0*(newData)/(2**16)
    print "                             newHumid: " + str(newHumid)

    oldHumid = -6.0 + 125.0*(oldData)/(2**16)
    print "                             oldHumid: " + str(oldHumid)
'''

    #return humid

#print "%.2f" %(sensorHumid(0,2))

#sensorHumid(0,2)
