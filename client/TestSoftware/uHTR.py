# uHTR_Test.py

import Hardware
import DChain
import DaisyChain
import os
import sys
import time 
import multiprocessing as mp
from subprocess import Popen, PIPE
from commands import getoutput
from ROOT import *
gROOT.SetBatch()

class uHTR_Test:
	def __init__(self, uhtr_slots, qcard_slots):
		self.master_dict={}
		### Each key of master_dict corresponds to a QIE chip
		### The name of each QIE is "(qcard_slot, register)"
		### Each QIE chip returns a dictionary containing test results and its uHTR mapping
		### List of keys: "slot" "link" "channel" ........		

		self.hw = Hardware(qcard_slots)	#Array of RMs for communicating with DaisyChains

		self.crate=41			#Always 41 for summer 2016 QIE testing

		if isintance(uhtr_slots, int): self.uhtr_slots=[uhtr_slots]
		else: self.uhtr_slots=uhtr_slots
		
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
	
	def add_QIE(self, qcard_slot, register, uhtr_slot, link, channel):
		QIE_info["uhtr_slot"]=uhtr_slot
		QIE_info["link"]=link		
		QIE_info["channel"]=channel
		
		key="({0}, {1})".format(qcard_slot, register)
		self.master_dict[key]=QIE_info
		

#############################################################

#############################################################
# Higher level uHTR test functions
# Results of each test recorded in master_dict
#############################################################


# eventually we might write functions that can actually be used to test things





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
                for uhtr_slot, uhtr_slot_results in test_results.iteritems():
                        for chip, chip_results in uhtr_slot_results.iteritems():
				if chip_results["pedBinMax"] > 12:
					return (int(uhtr_slot), chip_results["link"], chip_results["channel"])
		print "Mapping failed"
	
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
		

	
	def uHTRtool_source_test(self):
	        ### checks to see if the uHTRtool is sourced, and sources it if needed	
		uhtr_cmd="uHTRtool.exe"
		error="sh: uHTRtool.exe: command not found"
		check=getoutput(uhtr_cmd)
		source_cmd=["source /home/daqowner/dist/etc/env.sh"]

		if check==error:
			print "WARNING, you need to run 'source ~daqowner/dist/etc/env.sh' before you can use uHTRtool.exe"
		
#############################################################


#############################################################
# Non-member functions used to generate and read histos


def uHTRtool_source_test():
	### checks to see if the uHTRtool is sourced, and sources it if needed	
	uhtr_cmd="uHTRtool.exe"
	error="sh: uHTRtool.exe: command not found"
	check=getoutput(uhtr_cmd)
	source_cmd=["source /home/daqowner/dist/etc/env.sh"]

	if check==error:
		print "WARNING, you need to run 'source ~daqowner/dist/etc/env.sh' before you can use uHTRtool.exe"

	return None

def send_commands(crate=None, slot=None, cmds=''):
	# Sends commands to "uHTRtool.exe" and returns the raw output and a log. The input is the crate number, slot number, and a list of commands.
	# Arguments and variables:
	raw = ""
	results = {}                # Results will be indexed by uHTR IP unless a "ts" has been specified, in which case they'll be indexed by (crate, slot).

	## Parse cmds:
	if isinstance(cmds, str):
		print 'WARNING (uhtr.send_commands): You probably didn\'t intend to run "uHTRtool.exe" with only one command: {0}'.format(cmds)
		cmds = [cmds]

	# Prepare ip address:uhtr_ip = "192.168.%i.%i"%(crate, slot*4)
	uhtr_ip = "192.168.%i.%i"%(crate, slot*4)

	# Prepare the uHTRtool arguments:
	uhtr_cmd = "uHTRtool.exe {0}".format(uhtr_ip)   

	# Send commands and organize results:
	# This puts the output of the command into a list called "raw_output" the first element of the list is stdout, the second is stderr.
	raw_output = Popen(['printf "{0}" | {1}'.format(' '.join(cmds), uhtr_cmd)], shell = True, stdout = PIPE, stderr = PIPE).communicate()
	raw += raw_output[0] + raw_output[1]
	results[uhtr_ip] = raw
	return results

def get_histo(crate, slot, n_orbits=5000, sepCapID=0, file_out=""):
        # Set up some variables:
        log = ""
        if not file_out:
                file_out = "histo_uhtr{0}.root".format(slot)

        # Histogram:
        cmds = [
                '0',
                'link',
                'histo',
                'integrate',
                '{0}'.format(n_orbits),                # number of orbits to integrate over
                '{0}'.format(sepCapID),
                '{0}'.format(file_out),
                '0',
                'quit',
                'quit',
                'exit',
                '-1'
        ]
        result = send_commands(crate=crate, slot=slot, cmds=cmds)
        return result
	
def generate_histos(crates, slots, n_orbits=5000, sepCapID=0, file_out_base="", out_dir="histotests"):

	###check for single crate/single slot	
	if isinstance(crates, int):
		crates=[crates]

	if isinstance(slots, int):
		slots=[slots] 
	
	if not file_out_base:
		file_out_base="uHTR_histotest"

	cwd=os.getcwd()

	### check to see if out_dir exists and set it up if it does
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	dir_path="{0}/{1}".format(cwd, out_dir)
	os.chdir(dir_path)

	for crate in crates:
		for slot in slots:
			file_out=file_out_base+"_{0}_{1}.root".format(crate, slot)
			p = mp.Process(target=get_histo, args=(crate, slot, n_orbits, sepCapID, file_out,))
			p.start()

	while mp.active_children():
		time.sleep(0.1)

	print "All tests complete"	
			
	os.chdir(cwd)	

	### return the the full path to out_dir
	return dir_path

def getHistoInfo(file_in="", sepCapID=False, signal=False, qieRange = 0):
	slot_result = {}
	f = TFile(file_in, "READ")
	if sepCapID:
		rangeADCoffset = qieRange*64.
		for i_link in range(24):
			for i_ch in range(6):
				histNum = 6*i_link + i_ch
				h = f.Get("h%d"%(histNum))
				chip_results = {}
				chip_results["link"] = i_link
				chip_results["channel"] = i_ch
				chip_results["binMax"] = []
				chip_results["RMS"] = []
				for i_capID in range(4):
					offset = 64*(i_capID)
					h.GetXaxis().SetRangeUser(offset, offset+63)
					chip_results["RMS"].append(max(h.GetRMS(), 0.01))

				slot_result[histNum] = chip_results
		
	else:
                if signal:
			for i_link in range(24):
				for i_ch in range(6):
					histNum = 6*i_link + i_ch
					h = f.Get("h%d"%(histNum))
					lastBin = h.GetSize() - 3
					chip_results = {}
					chip_results["link"] = i_link
					chip_results["channel"] = i_ch
                                        #Transition from pedestal to signal is consistently around 10
                                        h.GetXaxis().SetRangeUser(7,13)
                                        cutoff = h.GetMinimum()
					h.GetXaxis().SetRangeUser(0,cutoff)
					binMax = h.GetMaximumBin()
					chip_results["pedBinMax"] = h.GetBinContent(binMax) 
					chip_results["pedRMS"] = h.GetRMS()
					h.GetXaxis().SetRangeUser(cutoff,lastBin)
					binMax = h.GetMaximumBin()
					chip_results["signalBinMax"] = h.GetBinContent(binMax)
					chip_results["signalRMS"] = h.GetRMS()

					slot_result[histNum] = chip_results

                else:
                        for i_link in range(24):
                                for i_ch in range(6):
                                        histNum = 6*i_link + i_ch
                                        h = f.Get("h%d"%(histNum))
                                        chip_results = {}
                                       	chip_results["link"] = i_link
					chip_results["channel"] = i_ch
					chip_results["pedBinMax"] = h.GetMaximumBin() 
					chip_results["pedRMS"] = h.GetRMS()
					
                                        slot_result[histNum] = chip_results
 
	f.Close()
	return slot_result
	
