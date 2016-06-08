from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

def sensor(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x05,0,0,0])
    print "Now for the sensor:\n"
    b.write(0x40,[0xf3])
    b.read(0x40,2) #what happens if I read 4 bytes? trash?

    data = b.sendBatch()[2]
    data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
    return data

#print "Sensor: " + sensor(0,0)
temp = (-46.85) +175.72*(sensor(0,0))/(2**16)
print "%.2f" %temp
#print "Sensor:" + sensor(0,0)

#(-46.85) +175.72*(TEMP)/(2**16)

'''
#/usr/bin/python
#
#testTuesday.py
#a test input file for the client
################################################################################
# imports - must have in all files using these commands
################################################################################

#from client import webBus
from client import webBus
import QIELib

b = webBus("pi5")
#Available functions: b.write, b.read, b.sendBatch, b.sleep

def readSensor():
    #Open GPIO from fanboard to ngCCM to access RM 1,2 (J1-J12)
    b.write(0x72,[0x02])
    #Open ngCCM mux to I2C group 2 (RM 1, J2-J5)
    b.write(0x74,[0x02])
    #Trying to communicate with the SHT21 sensor (should be 5?...)
    b.write(0x19,[0x11,0x05,0,0,0])
    #tell the sensor to test for temperature in "hold more" (1110'0011 = 0xe3)
    b.write(0x40, [0x3e])
    #read the 2 data bytes on temp
    b.read(0x40,2)
    #obtain the read-in temp info
    temp = b.sendBatch[5]


    b.write(0x19,[0x11,0x05,0,0,0])
    #tell the sensor to test for temperature in "hold more" (1110'0011 = 0xe3)
    b.write(0x40,[0xe3])
    b.read(0x40,2) #read the 2 data bytes on temp
    #tell the sensor to test for humidity in "hold mode" (1110'0101 = 0xe5)
    b.write(0x40,[0xe5])
    b.read(0x40,2) #read the 2 data bytes on relative humidity



####################################################
#Caleb's Code from uniqueID.py
####################################################

# Read UniqueID
def uniqueID(jslot):
    # Open channel to ngCCM for RM1,2, J1 - J12
    i2c_write(0x72,[0x02])
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])
    # Read UniqueID 8 bytes from SSN for first QIE in J2
    # Note that the i2c_select has register address 0x11
    # Note that the SSN expects 32 bits (4 bytes)
    i2c_write(0x19,[0x11,0x04,0,0,0])
    i2c_read(0x50,8)

def helloQIE(jslot):
    # Open channel to ngCCM for RM1,2, J1 - J12
    i2c_write(0x72,[0x02])
    # Open channel to i2c group 2, J2 - J5
    i2c_write(0x74,[0x02])
    # Note that the QIEs for one half have register address 0x30
    # Note that the QIEs for the other half have register address 0x31
    # Note that the QIE expects 384 bits (48 bytes)
    # 384 bits = 64 bits * 6 qie cards = 8 bytes * 6 qie cards
    i2c_write(0x19,[0x30])
    i2c_read(0x30,48)
'''
