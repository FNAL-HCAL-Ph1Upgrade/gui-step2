from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

def vttxOpen(rm,slot):
    q.openChannel(rm,slot)
    #VTTX 1 is value "1" in I2C_SELECT table
    b.write(q.QIEi2c[slot],[0x11,0x01,0,0,0])
    b.sendBatch()

vttxOpen(0,0)
