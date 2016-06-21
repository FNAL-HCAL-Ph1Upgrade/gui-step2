# uHTR_Test.py

from histo_generator import *
from histo_reader import *
import TestStand
import os

class uHTR_Test:
	def __init__(self, slots, ts):
		self.master_dict={}
		### Each key of master_dict corresponds to a QIE chip
		### The name of each QIE is "(qcard_slot, register)"
		### Each QIE chip returns a dictionary containing test results and its uHTR mapping
		### List of keys: "slot" "link" "channel" ........		

		self.ts=ts		#TestStand object for communicating with DaisyChains

		self.crate=41		#Always 41 for summer 2016 QIE testing

		if isintance(slots, int): self.slots=[slots]
		else: self.slots=slots
		
#		self.QIE_mapping()

#############################################################
# Adding and extracting data from the master_dict
#############################################################	
	
	def get_QIE(self, qcard_slot, register):
		### Returns the dictionary storing the test results of the specified QIE chip
		key="({0}, {1})".format(qcard_slot, register)
		return self.master_dict[key]
	
	def get_QIE_results(self, qcard_slot, register, test_key=""):
		### Returns the (pass, fail) tuple of specific test
		QIE=self.get_QIE(qcard_slot, register)
		return QIE[test_key]
	
	def add_QIE(self, qcard_slot, register, slot, link, channel):
		QIE_info["slot"]=slot
		QIE_info["link"]=link		
		QIE_info["channel"]=channel
		
		key="({0}, {1})".format(qcard_slot, register)
		self.master_dict[key]=QIE_info
		

#############################################################


#############################################################
# Mapping functions
#############################################################

       def QIE_mapping(self):
                # Records the uHTR slot, link, and channel of each QIE in master_dict
               for rm in self.ts.RMs:
			for dChain in rm.dChains: 
                	       # change settings of chian[0]
				info=self.get_mapping_histo()
				self.add_QIE(qcard_slot, register, info[0], info[1], info[2])


        def get_mapping_histo(self):
                # matches histo to QIE chip for mapping
                test_results=self.get_histo_results()
                for slot, slot_results in test_results.iteritems():
                        for chip, chip_results in slot_results.iteritems():
				if chip_results["pedBinMax"] > 12:
					return (int(slot), chip_results["link"], chip_results["channel"])
		print "Mapping failed. You suck"
	
#############################################################

#############################################################
# Basic uHTRtool functions 
# Should only be used by higher level tests 
#############################################################

	def get_histo_results(self, crate=None, slots=None, n_orbits=1000, sepCapID=0, signalOn=0, out_dir="histotest"):
		# Runs uHTRtool.exe and returns layered ditctionary of results. 
		if slots is None:
			slots=self.slots		
		if crate is None:
			crate=self.crate


		test_results = {}
		path_to_root = generate_histos(crate, slots, n_orbits, sepCapID, out_dir= out_dir)
		
		for file in os.listdir(path_to_root):
			
			# Extract slot number from file name
			temp = file.split('_')
			temp = temp[-1].split('.root')
			slot_num = str(temp[0])
			
			test_results["%s"%(slot_num)] = getHistoInfo(signal=signalOn, file_in=path_to_root+"/"+file)
		
		os.removedirs(path_to_root)
		
		return test_results
		
		def source_test(self):
			source_test()
		
#############################################################




#############################################################
# Higher level uHTR test functions
# Results of each test recorded in master_dict
#############################################################


# eventually we might write functions that can actually be used to test things





#############################################################


if __name__=="__main__":
	active_slots=[2, 3, 5, 7, 18, 20] 
	ts=TestStand(active_slots)
	str(ts)


