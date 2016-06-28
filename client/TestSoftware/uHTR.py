# uHTR.py

import Hardware as hw
from DChains import DChains
from DaisyChain import DaisyChain
from QIE import QIE
import os
import sys
import time
import numpy 
import multiprocessing as mp
from subprocess import Popen, PIPE
from commands import getoutput
from ROOT import *
gROOT.SetBatch()


if __name__ == "__main__":

	from client import webBus
	from uHTR import uHTR

	qcard_slots = [2, 5]
	b = webBus("pi6", 0)
	uhtr = uHTR(6, qcard_slots, b)
	for slot in qcard_slots:
		for chip in xrange(12):
			info=uhtr.get_QIE_map(slot, chip)
			print "Q_slot: {4}, Qie: {3}, uhtr_slot: {0}, link: {1}, channel: {2}".format(info[0],info[1],info[2],chip,slot)



class uHTR():
	def __init__(self, uhtr_slots, qcard_slots, bus):
	
		self.crate=41			#Always 41 for summer 2016 QIE testing

		if isinstance(uhtr_slots, int): self.uhtr_slots=[uhtr_slots]
		else: self.uhtr_slots=uhtr_slots

		self.bus=bus

		self.qcards=qcard_slots

		self.master_dict={}
		### Each key of master_dict corresponds to a QIE chip
		### The name of each QIE is "(qcard_slot, chip)"
		### Each QIE chip returns a dictionary containing test results and its uHTR mapping
		### List of keys: "slot" "link" "channel" "ped_test"	
	
		
		# setup functions
		clock_setup(self.crate, qcard_slots)
		for slot in self.uhtr_slots:
			init_links(self.crate, slot)
		self.QIE_mapping()
		
#############################################################
# Higher level uHTR test functions
# Results of each test recorded in master_dict
#############################################################

	def ped_test(self):
		for setting in list(i-31 for i in xrange(63)):
			for qslot in self.qcards:
				dc=hw.getDChains(qslot, self.bus)
				dc.read()
				for i in xrange(12):
					dc[i].PedastalDAC[setting]
				dc.write()
				dc.read()
			info=get_histo_results(self.crate, self.uhtr_slots)
			

#############################################################


#############################################################
# Adding and extracting data from the master_dict
#############################################################	
	
	def get_QIE(self, qcard_slot, chip):
		### Returns the dictionary storing the test results of the specified QIE chip
		key="({0}, {1})".format(qcard_slot, chip)
		return self.master_dict[key]
	
	def get_QIE_results(self, qcard_slot, chip, test_key=""):
		### Returns the (pass, fail) tuple of specific test
		QIE=self.get_QIE(qcard_slot, chip)
		return QIE[test_key]
	
	def get_QIE_map(self, qcard_slot, chip):
		key="({0}, {1})".format(qcard_slot, chip)
                qie=self.master_dict[key]
		slot=qie["uhtr_slot"]
		link=qie["link"]
		channel=qie["channel"]
		return (slot, link, channel)

	def add_QIE(self, qcard_slot, chip, uhtr_slot, link, channel):
		QIE_info={}
		QIE_info["uhtr_slot"]=uhtr_slot
		QIE_info["link"]=link		
		QIE_info["channel"]=channel
		
		key="({0}, {1})".format(qcard_slot, chip)
		self.master_dict[key]=QIE_info
		

#############################################################

 
#############################################################
# Mapping functions
#############################################################

	def QIE_mapping(self):
		# Records the uHTR slot, link, and channel of each QIE in master_dict
		for qslot in self.qcards:
			dc=hw.getDChains(qslot, self.bus)
			hw.SetQInjMode(0, qslot, self.bus)
			dc.read()
			for chip in [0,6]:
				for num in xrange(12):
					dc[num].PedastalDAC(-9)
					if num==chip:
						dc[num].PedastalDAC(31)
				dc.write()
				dc.read()
				info=self.get_mapping_histo()
				if info is not None:
					uhtr_slot=info[0]
					link=info[1]
					for i in xrange(6):
						self.add_QIE(qslot, chip+i, uhtr_slot, link, 5-i)
				else: print "mapping failed"
			for num in xrange(12):
				dc[num].PedastalDAC(-9)
				dc.write()
				dc.read()


	def get_mapping_histo(self):
		# matches histo to QIE chip for mapping
		map_results=self.get_histo_results(out_dir="map_test")
		for uhtr_slot, uhtr_slot_results in map_results.iteritems():
			for chip, chip_results in uhtr_slot_results.iteritems():
				if chip_results["pedBinMax"] > 15:
					return (int(uhtr_slot), chip_results["link"], chip_results["channel"])
		return None
	
#############################################################


#############################################################
# Other non-testing funtions 
# Mainly used by higher level to make/read histos
#############################################################


	def uHTRtool_source_test():
	        ### checks to see if the uHTRtool is sourced, and sources it if needed	
		uhtr_cmd="uHTRtool.exe"
		error="sh: uHTRtool.exe: command not found"
		check=getoutput(uhtr_cmd)
		source_cmd=["source /home/daqowner/dist/etc/env.sh"]

		if check==error:
			print "WARNING, you need to run 'source ~daqowner/dist/etc/env.sh' before you can use uHTRtool.exe"


	def get_histo_results(self, crate=None, slots=None, n_orbits=1000, sepCapID=0, signalOn=0, out_dir="histotest"):
		# Runs uHTRtool.exe and returns layered ditctionary of results. 
		if slots is None:
			slots=self.uhtr_slots
		if crate is None:
			crate=self.crate
		histo_results = {}
		path_to_root = generate_histos(crate, slots, n_orbits, sepCapID, out_dir=out_dir)
		for file in os.listdir(path_to_root):
			# Extract slot number from file name
			temp = file.split('_')
			temp = temp[-1].split('.root')
			slot_num = str(temp[0])
			
			histo_results[slot_num] = getHistoInfo(signal=signalOn, file_in=path_to_root+"/"+file)
#		os.removedirs(path_to_root)		
		return histo_results
		

#############################################################

def generate_histos(crate, slots, n_orbits=5000, sepCapID=0, file_out_base="", out_dir="histotests"):
	#can only generate over a single crate
	if not file_out_base:
		file_out_base="uHTR_histotest"
	cwd=os.getcwd()
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	dir_path="{0}/{1}".format(cwd, out_dir)
	os.chdir(dir_path)

	for slot in slots:
		file_out=file_out_base+"_{0}_{1}.root".format(crate, slot)
		p = mp.Process(target=get_histo, args=(crate, slot, n_orbits, sepCapID, file_out,))
		p.start()

	while mp.active_children():
		time.sleep(0.1)	
	
	os.chdir(cwd)	
	return dir_path
		
def send_commands(crate=None, slot=None, cmds=''):
	# Sends commands to "uHTRtool.exe" and returns the raw output and a log. The input is the crate number, slot number, and a list of commands.
	raw = ""
	results = {}

	if isinstance(cmds, str):
		print 'WARNING (uhtr.send_commands): You probably didn\'t intend to run "uHTRtool.exe" with only one command: {0}'.format(cmds)
		cmds = [cmds]

	uhtr_ip = "192.168.{0}.{1}".format(crate, slot*4)
	uhtr_cmd = "uHTRtool.exe {0}".format(uhtr_ip)   
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


def clock_setup(crate, slots):
	cmds = [
		'0'
		'clock'
		'setup'
		'3'
		'quit'
		'exit'
		]
	for slot in slots:
		send_commands(crate=crate, slot=slot, cmds=cmds)
	

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



def init_links(crate, slot):
	linkInfo = get_link_info(crate, slot)
	onLinks, goodLinks, badLinks = check_link_status(linkInfo)
	if onLinks == 0:
		print "All crate %d, slot %d links are OFF! NOT initializing that slot!"%(crate,slot)
		return
	medianOrbitDelay = int(median_orbit_delay(linkInfo))
	if badLinks > 0:
		initCMDS = ["0","link","init","1","%d"%(medianOrbitDelay),"0","0","0","quit","exit"]
		send_commands(crate=crate, slot=slot, cmds=initCMDS)
		init_links(crate, slot)


def get_BCN_status(uHTRPrintOut):
	for key, value in uHTRPrintOut.iteritems():
		linesList = value.split("\n")
		BCNs = []
		for j in range(len(linesList)):
			if len(linesList[j].split("Align BCN")) == 2:
				BCNLine = filter(None, linesList[j].split("Align BCN"))
				BCNList = filter(None, BCNLine[0].split(" "))
				BCNList = map(int, BCNList)
				BCNs = BCNs + BCNList
	return BCNs 


def get_ON_links(uHTRPrintOut):
	for key, value in uHTRPrintOut.iteritems():
		linesList = value.split("\n")
		ONLinks = []
		for j in range(len(linesList)):
			if len(linesList[j].split("BadCounter")) == 2:
				ONLine = filter(None, linesList[j].split("BadCounter"))
				ONList = filter(None, ONLine[0].split(" "))
				ONLinks = ONLinks + ONList
	return ONLinks


def get_BPR_status(uHTRPrintOut):
	for key, value in uHTRPrintOut.iteritems():
		linesList = value.split("\n")
		BPRs = []
		for j in range(len(linesList)):
			if len(linesList[j].split("BPR Status")) == 2:
				BPRLine = filter(None, linesList[j].split("BPR Status"))
				BPRList = filter(None, BPRLine[0].split(" "))
				BPRs = BPRs + BPRList
	return BPRs


def get_AOD_status(uHTRPrintOut):
	for key, value in uHTRPrintOut.iteritems():
		linesList = value.split("\n")
		AODs = []
		for j in range(len(linesList)):
			if len(linesList[j].split("AOD Status")) == 2:
				AODLine = filter(None, linesList[j].split("AOD Status"))
				AODList = filter(None, AODLine[0].split(" "))
				AODs = AODs + AODList
	return AODs


def median_orbit_delay(linkInfo):
	BCNList = []
	for k in range(len(linkInfo["BCN Status"])):
		if linkInfo["ON Status"][k] == "ON":
			BCNList = BCNList + [linkInfo["BCN Status"][k]]	
	BCNMedian = int(numpy.median(BCNList))
	return BCNMedian

		
def check_link_status(linkInfo):
	goodLinks = 0
	badLinks = 0
	onLinks = 0
	for l in range(len(linkInfo["BPR Status"])):
		if linkInfo["ON Status"][l] == "ON":
			onLinks += 1
		if linkInfo["BPR Status"][l] == "111" and linkInfo["AOD Status"][l] == "111" and linkInfo["ON Status"][l] == "ON":
			goodLinks += 1
		elif linkInfo["ON Status"][l] == "ON" and not (linkInfo["BPR Status"][l] == "111" and linkInfo["AOD Status"][l] == "111"):
			badLinks += 1

	return onLinks, goodLinks, badLinks 


def get_link_info(crate, slot):
	linkInfo = {}
        statCMDs = ["0", "link", "status", "quit", "exit"]
        statsPrintOut = send_commands(crate=crate, slot=slot, cmds=statCMDs)
        linkInfo["BCN Status"] = get_BCN_status(statsPrintOut)
        linkInfo["BPR Status"] = get_BPR_status(statsPrintOut)
        linkInfo["AOD Status"] = get_AOD_status(statsPrintOut)
        linkInfo["ON Status"] = get_ON_links(statsPrintOut)
	return linkInfo


