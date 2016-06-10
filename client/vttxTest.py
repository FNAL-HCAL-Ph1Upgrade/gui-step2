from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

########################################################
# VTTX Read Functions
########################################################

def vttx1read(rm,slot):
    q.openChannel(rm,slot)
    #VTTX 1 is value "1" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x01,0,0,0])
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    data = b.sendBatch()[2]

    return data

def vttx2read(rm,slot):
    q.openChannel(rm,slot)
    #VTTX 1 is value "1" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x02,0,0,0])
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    data = b.sendBatch()[2]

    return data



########################################################
# VTTX Write Functions
########################################################

def vttx1write(rm,slot):
    q.openChannel(rm,slot)
    #VTTX 1 is value "1" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x01,0,0,0])
    b.write(0x7E,[0x00,0x87,0x99,0x19,0x88,0xff,0xff,0x04])
    data = b.sendBatch()[1]

    return data

def vttx2write(rm,slot):
    q.openChannel(rm,slot)
    #VTTX 1 is value "1" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x02,0,0,0])
    b.write(0x7E,[0x00,0x87,0x99,0x19,0x88,0xff,0xff,0x04])
    data = b.sendBatch()[1]

    return data

print "From vttx1read: " + vttx1read(0,0)
print "From vttx2read: " + vttx2read(0,0)

print "From vttx1write: " + vttx1write(0,0)
print "From vttx2write: " + vttx2write(0,0)

print "From vttx1read: " + vttx1read(0,0)
print "From vttx2read: " + vttx2read(0,0)


# output of successful execution of the code!
'''
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 1 0 0 0
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 135 153 25 136 255 255 4
From vttx1read: 135 153 25 136 255 255 4
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 2 0 0 0
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 135 153 25 136 255 255 4
From vttx2read: 135 153 25 136 255 255 4
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 1 0 0 0
    RECEIVED: 0
    SENT: w 126 0 135 153 25 136 255 255 4
    RECEIVED: 0
From vttx1write: 0
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 2 0 0 0
    RECEIVED: 0
    SENT: w 126 0 135 153 25 136 255 255 4
    RECEIVED: 0
From vttx2write: 0
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 1 0 0 0
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 135 153 25 136 255 255 4
From vttx1read: 135 153 25 136 255 255 4
    ##### RM in 0,1 #####
    SENT: w 114 2
    RECEIVED: 0
    ##### open i2c #####
    SENT: w 116 2
    RECEIVED: 0
    SENT: w 25 17 2 0 0 0
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 135 153 25 136 255 255 4
From vttx2read: 135 153 25 136 255 255 4
'''
