from client import webBus
import QIELib
b = webBus("pi5",0)
q = QIELib


#returns the temperature of the QIE card
def sensorTemp(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    #Splitting the incoming data and reversing the order of bytes
    #(the read function's inherent reversal of bytes isn't compatible with
    #this particular sensor's desired output order)

    data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
    #Converting the temperature using equation
    temp = (-46.85) +175.72*(data)/(2**16)

    return temp

print "%.2f" %(sensorTemp(0,2))


#returns the relative humidity of the QIE card
def sensorHumid(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xe5])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    #Splitting the incoming data and reversing the order of bytes
    #(the read function's inherent reversal of bytes isn't compatible with
    #this particular sensor's desired output order)

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


    #return humid

#print "%.2f" %(sensorHumid(0,2))

sensorHumid(0,2)
