from client import webBus
import QIELib
import IglooLib

b = webBus("pi5",0) #can add "pi5,0" so won't print send/receive messages
q = QIELib

class Test:
    def __init__(self, bus, address, logfile, iterations = 1):
        self.bus = bus
        self.address = address
        self.logstream = logfile #changed from logstream to logfile
        self.iterations = iterations
    def run(self):
        passes = 0
        for i in xrange(self.iterations): #changed from iterations to self.iterations
            if self.testBody() == True: passes += 1 #changed true to True
        return (passes, self.iterations - passes) #changed fails to (self.iterations - passes)
    def log(self, message):
        logprint(message, file=self.logfile)
    def testBody(self):
        return True

# helpful string decimal to string hex
def strToHex(string):
        catBinary = ""
        j=0
        for i in string.split():
                catBinary = catBinary + " " + hex(int(string.split()[j]))[2:]
                j = j + 1
        return catBinary

class vttx1RWR(Test):


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

def run():
    def openVttx(rm,slot):
        q.openChannel(rm,slot)
        #the igloo is value "3" in I2C_SELECT table
        b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
        b.sendBatch()
    openIgloo(0,0)
