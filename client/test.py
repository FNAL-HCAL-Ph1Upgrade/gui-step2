from client import webBus

b = webBus("pi4")

b.read(0x72, 1)
print b.sendBatch()

