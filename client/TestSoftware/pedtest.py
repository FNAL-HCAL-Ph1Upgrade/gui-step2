from uHTR import *
from client import webBus
from Hardware import *

bus=webBus("pi6",0)

for num in list(i-31 for i in xrange(63)):
	file_out="ped_{0}".format(num)
	dc=hw.getDChains(21,bus)
	dc.read()
	for i in xrange(12):
		dc[i].PedastalDAC[num]
	dc.write()
	dc.read()
	generate_histos(41, 6, file_out_base=file_out, out_dir="ped_test")


