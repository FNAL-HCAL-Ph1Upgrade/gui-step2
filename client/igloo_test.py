from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

def igloo(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x11,0x03,0,0,0])
    # b.write(0x09,[0x05])
    # b.read(0x09,8)

igloo(0,0)
