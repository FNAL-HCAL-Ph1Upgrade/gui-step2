from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

'''
def regTest(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x30])
    b.read(0x30,48)
    temp = b.sendBatch()[1]

    return temp

print regTest(0,2)

'''


#returns the temperature of the QIE card
def sensorTemp(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    b.write(0x40,[0xf3])
    b.read(0x40,2)

    data = b.sendBatch()[2]
    data = int((hex(int(data.split()[1])))[2:] + (hex(int(data.split()[0])))[2:],16)
    #Converting the temperature using equation
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

    data = int((hex(int(data.split()[1])))[2:] + (hex(int(data.split()[0])))[2:],16)
    #Converting the humidity using equation
    humid = -6 + 125.0*(data)/(2**16)

    return humid

print "%.2f" %(sensorHumid(0,2))
