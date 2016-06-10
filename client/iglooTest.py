'''
Goals:
* understand the "spy" register (probably the 200-bit one)
* try to write to a "read only" register and ensure that it didn't work
    * but first, read what's there so that in case you overwrite, you can undo your mistakes...
* understand the SERDES registers (see Microsemi documentation for meanings)
* create functions to read (and if possible) write to internal registers

'''

from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

def openIgloo(rm,slot):
    q.openChannel(rm,slot)
    #the igloo is value "3" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
    b.sendBatch()

##################################
# Register bytes 0x00 - 0x01 (Read only)
##################################
def readFPGAVersion():
    #openIgloo should already be called before this
    b.write(0x09,0x00)
    b.read(0x09,8) # "fpga major version"
    majVer = b.sendBatch()[1]

    b.write(0x09,0x01)
    b.read(0x09,8) # "fpga minor verison"
    minVer = b.sendBatch()[1]

    return "majVer: " + majVer + "  minVer: " + minVer

openIgloo(0,0)
print readFPGAVersion()

##########################
# The Igloo2 class
##########################

#class Igloo:

    ###########################
    # Register Functions
    ###########################
