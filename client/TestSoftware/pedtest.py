from uHTR import *
import os


histo_results = {}
path_to_root = 
for file in os.listdir(path_to_root):
	# Extract slot number from file name
        temp = file.split('_')
        temp = temp[-1].split('.root')
        slot_num = str(temp[0])
        histo_results[slot_num] = getHistoInfo(signal=signalOn, file_in=path_to_root+"/"+file)
#       os.removedirs(path_to_root)
        
for uhtr_slot, uhtr_slot_results in histo_results.iteritems():
	for chip, chip_results in uhtr_slot_results.iteritems():
        	key="({0}, {1}, {2})".format(uhtr_slot, chip_results["link"], chip_results["channel"])
                if setting == -31: ped_results[key]=[]
                ped_results[key].append(chip_results["pedBinMax"])
cwd=os.getcwd()
os.makedirs("ped_plots")
os.chdir(cwd  + "/ped_plots")
for qslot in self.qcards:
	for chip in xrange(12):
        	ped_key = str(self.get_QIE_map(qslot, chip))
                chip_arr = ped_results[ped_key]
                slope = analyze_results(ped_settings, chip_arr, ped_key)
                print "qslot: {0}, chip: {1}, slope: {2}".format(qslot, chip, slope)
 os.chdir(cwd)

