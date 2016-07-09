from client import webBus
import QIELib
b = webBus("pi5",0)
q = QIELib

# helpful string decimal to string hex
def strToHex(string):
        catBinary = ""
        j=0
        for i in string.split():
                catBinary = catBinary + " " + hex(int(string.split()[j]))[2:]
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


########################################################
# VTTX Read/Write/Read Functions
########################################################

# Read from Vttx1, write that same set of bytes, read again to confirm
def vttx1RWR(rm, slot):
    # First, read from vttx1 LDD to ascertain the register values
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x01,0,0,0])
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    read1 = b.sendBatch()[2] # store read data into "read1"

    readArr = read1.split()
    writeArr = list(int(i) for i in readArr)

    # write to vttx1 what we just read from it
    b.write(0x7E,[0x00] + writeArr)
    b.sendBatch()

    # read from vttx1 to check if it worked
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    read2 = b.sendBatch()[1]

    # if read1 matches read2, then write was successful -- print register
    if (read1 == read2):
        return "Pass, Reg = " + strToHex(read2)
    else:
        return "Fail"

# Read from Vttx2, write that same set of bytes, read again to confirm
def vttx2RWR(rm, slot):
    # First, read from vttx1 LDD to ascertain the register values
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x02,0,0,0])
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    read1 = b.sendBatch()[2] # store read data into "read1"

    readArr = read1.split()
    writeArr = list(int(i) for i in readArr)

    # write to vttx2 what we just read from it
    b.write(0x7E,[0x00] + writeArr)
    b.sendBatch()

    # read from vttx2 to check if it worked
    b.write(0x7E,[0x00])
    b.read(0x7E,7)
    read2 = b.sendBatch()[1]

    # if read1 matches read2, then write was successful -- print register
    if (read1 == read2):
        return "Pass, Reg = " + strToHex(read2)
    else:
        return "Fail"


print 'From RWR of vttx1: ' + vttx1RWR(0,0)
print 'From RWR of vttx2: ' + vttx2RWR(0,0)


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
    RECEIVED: 4 255 255 136 25 153 7
    SENT: w 126 0 4 255 255 136 25 153 7
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 4 255 255 136 25 153 7
From RWR of vttx1: Pass, Reg =  4 ff ff 88 19 99 7
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
    SENT: w 126 0 135 153 25 136 255 255 4
    RECEIVED: 0
    SENT: w 126 0
    RECEIVED: 0
    SENT: r 126 7
    RECEIVED: 135 153 25 136 255 255 4
From RWR of vttx2: Pass, Reg =  87 99 19 88 ff ff 4
'''
