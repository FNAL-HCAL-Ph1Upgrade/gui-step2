from client import webBus
import QIELib
b = webBus("pi5")
q = QIELib

def bridge(rm,slot):
    q.openChannel(rm,slot)
    b.write(q.QIEi2c[slot],[0x00])
    b.read(q.QIEi2c[slot],4)
    return b.sendBatch()[-1]

print bridge(0,0)
