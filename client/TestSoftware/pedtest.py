from uHTR import *
from client import webBus
import Hardware as hw 
from DChains import DChains
import os

bus=webBus("pi5",0)
slots=[2, 5]
ped_arr=[]

for num in list(i-31 for i in xrange(63)):
	file_out="ped_{0}".format(num)
	for slot in slots:
		dc=hw.getDChains(slot, bus)
		dc.read()
		for i in xrange(12):
			dc[i].PedestalDAC(num)
		dc.write()
		dc.read()
	generate_histos(41, [1], file_out_base=file_out, out_dir="ped_test")

	cwd=os.getcwd()
	os.chdir(cwd+"/ped_test")
	info=getHistoInfo(file_in=file_out+"_41_1.root")
	setting_arr=[]
	for chip, chip_results in info.iteritems():
		if chip_results["pedBinMax"] != 1:
			setting_arr.append(chip_results["pedBinMax"])
	print "setting {0}".format(num)
	print setting_arr
	if len(setting_arr) != 0:
		ped_arr.append(float(sum(setting_arr))/float(len(setting_arr)))
	else: ped_arr.append(0)
	os.chdir(cwd)
print "all the setting averages"
for j, i in enumerate(ped_arr):
	print "ped {0} average:".format(j-31), i
