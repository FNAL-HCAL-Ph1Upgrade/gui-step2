from client import webBus
import QIELib
b = webBus("pi5",0)
q = QIELib


#returns the temperature of the QIE card
def sensorTemp(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,3)

    data = (b.sendBatch()[2]).split()
    checksum = data[2] # 3rd byte of data is the checksum
    print "Checksum: " + format(int(checksum),'08b')

    data = b.sendBatch()[2]
    #Splitting the incoming data and reversing the order of bytes
    #(the read function's inherent reversal of bytes isn't compatible with
    #this particular sensor's desired output order)

    # Splitting the incoming data & concatenating strings of binary bytes
    data = format(int(data.split()[0]),'08b') + format(int(data.split()[1]),'08b')
    print "2 data bytes: " + data
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting temp using equation
    temp = (-46.85) +175.72*(data)/(2**16)
    
    return temp

print "%.2f" %(sensorTemp(0,2))


#returns the relative humidity of the QIE card
def sensorHumid(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf5])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    # Splitting the incoming data & concatenating strings of binary bytes
    data = format(int(data.split()[0]),'08b') + format(int(data.split()[1]),'08b')
    # zero-ing out the 2 status bits, converting to int for calculations
    data = int(data[0:14] + "00", 2)
    # Converting humidity using equation
    humid = (-6.0) + 125.0 * (data)/(2**16)

    return humid

print "%.2f" %(sensorHumid(0,2))
