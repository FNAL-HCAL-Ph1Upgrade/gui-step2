from client import webBus
import TestSoftware.Hardware as Hardware

b = webBus("pi5",0)
h = Hardware


#returns the temperature of the QIE card
def sensorTemp(slot):

    h.openChannel(slot,b)
    b.write(h.getCardAddress(slot),[0x11,0x05,0,0,0])

    # q.openChannel(rm,slot)
    # b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,3)

    data = ((b.sendBatch()[2]).split())[1:]
    checksum = data[2] # 3rd byte of data is the checksum
    print 'Checksum: ' + hex(int(checksum))[2:]


# def checkCRC(data, checksum):
#   crc = 0
#   # calculates 8-Bit checksum with given polynomial
#   for i in range(0,2): # 2 data bytes total
#       crc ^= (data[i])
#       bit = 8
#       for i in range(0,8):
#           if (crc & )
#           bit -= 1
#     for
#  (u8t bit = 8; bit > 0;
# --
# bit)
#     {
# if
#  (crc & 0x80) crc = (crc << 1) ^ POLYNOMIAL;
# else
#  crc = (crc << 1);
#     }
#   }
# if
#  (crc != c
# hecksum)
# return
#  CHECKSUM_ERROR;
# else
# return
#  0;
# }

    # Splitting the incoming data & concatenating strings of binary bytes
    data = format(int(data[0]),'08b') + format(int(data[1]),'08b')
    print '2 data bytes: ' + data
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting temp using equation
    temp = (-46.85) +175.72*(data)/(2**16)
    return temp

print '%.2f' %(sensorTemp(5))


#returns the relative humidity of the QIE card
def sensorHumid(slot):
    # q.openChannel(rm,slot)
    # b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    h.openChannel(slot,b)
    b.write(h.getCardAddress(slot),[0x11,0x05,0,0,0])

    b.write(0x40,[0xf5])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    # Splitting the incoming data & concatenating strings of binary bytes
    # using [1] and [2] to skip over the error byte
    data = format(int(data.split()[1]),'08b') + format(int(data.split()[2]),'08b')
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting humidity using equation
    print 'data: '+str(data)
    humid = (-6.0) + 125.0 * (data)/(2**16)

    return humid

print '%.2f' %(sensorHumid(5))
