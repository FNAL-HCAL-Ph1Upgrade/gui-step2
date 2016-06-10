from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

# helpful string to hex list
def strToBin(string):
        catBinary = ""
        j=0
        for i in string.split():
                catBinary = catBinary + bin(int(string.split()[j]))[2:]
                print "j = " + str(j) + ",  catBinary = " + catBinary
                j = j + 1
        return catBinary

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
    #VTTX 2 is value "2" in I2C_SELECT table
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

# Read from Vttx, write that same set of bytes, read again to confirm
def vttx1RWR(rm, slot):
    #### READ
    read1 = vttx1read(rm, slot)
    readArr = read1.split()
    readArr.reverse()
    writeArr = list(int(i) for i in readArr)

    #### WRITE
    # write to vttx1 what we just read from it
    b.write(0x7E,[0x00,writeArr])

    #### READ
    #read from vttx1 to check if it worked
    read2 = vttx1read(rm,slot)

    if (read1 == read2):
        return "PASS!"
    else:
        return "YOU SHALL NOT PASS!"



print "From RWR of vttx1: " +vttx1RWR(0,0)




'''
print "From vttx1read: " + vttx1read(0,0)
print "From vttx2read: " + vttx2read(0,0)

print "From vttx1write: " + vttx1write(0,0)
print "From vttx2write: " + vttx2write(0,0)

print "From vttx1read: " + vttx1read(0,0)
print "From vttx2read: " + vttx2read(0,0)
'''

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
