from uHTR import uHTR
import Hardware as hw
from client import webBus
import DChains
import DaisyChain
import QIE


qcard_slots=[20, 21]
bus=webBus(serverAddress = "pi6", VERBOSITY=0)
uhtr=uHTR(6, qcard_slots, bus)

for i in qcard_slots:
	dc=hw.getDChains(i, bus)
	hw.openChannel(i, bus)
	dc.read()
	hw.SetQInjMode(1,i,bus)
	for j in xrange(12):
		qie=dc[j]
		qie.ChargeInjectDAC(8640)
		dc.write()
		info=uhtr.get_mapping_histo()
		if info is not None:
			print "Slot: {4} Qie: {3}, slot: {0}, link: {1}: channel: {2}".format(info[0], info[1], info[2], j, i)
	hw.SetQInjMode(0,i,bus)
