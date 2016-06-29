from uHTR import *
from client import webBus
from Hardware import *

bus=webBus("pi6",0)
slots=[21]

for num in list(i-31 for i in xrange(63)):
	file_out="ped_{0}".format(num)
	for slot in slots:
		dc=hw.getDChains(slots, bus)
		dc.read()
		for i in xrange(12):
			dc[i].PedestalDAC[num]
		dc.write()
		dc.read()
	generate_histos(41, 6, file_out_base=file_out, out_dir="ped_test")
	print "ped {0} done".format(num)

