# uHTR.py

import Hardware as hw
from DChains import DChains
from DaisyChain import DaisyChain
from QIE import QIE
import iglooClass_adry as i
import os
import sys
import time
import shutil
import numpy as np
import multiprocessing as mp
from subprocess import Popen, PIPE
from commands import getoutput
from collections import defaultdict
from datetime import datetime
import ROOT


if __name__ == "__main__":

	from client import webBus
	from uHTR import *
	uhtr_slots=[1, 2]
	all_slots = [2,3,4,5,7,8,9,10,18,19,20,21,23,24,25,26]
	qcard_slots=[2, 3, 4, 5]
	b = webBus("pi5", 0)
	uhtr = uHTR(uhtr_slots, qcard_slots, b)

	for slot in qcard_slots:
		for chip in xrange(12):
			info=uhtr.get_QIE_map(slot, chip)
			print "Q_slot: {4}, Qie: {3}, uhtr_slot: {0}, link: {1}, channel: {2}".format(info[0],info[1],info[2],chip,slot)
#	uhtr.ped_test()
#	uhtr.ci_test()
#	uhtr.phase_test()
	uhtr.shunt_test()


class uHTR():
	def __init__(self, uhtr_slots, qcard_slots, bus):

		self.uHTR_log = "{:%b%d%Y_%H%M%S}".format(datetime.now())

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
		clock_setup(self.crate, uhtr_slots)
		for slot in self.uhtr_slots:
			init_links(self.crate, slot)
		self.QIE_mapping()

		#make directory to put results histograms in
		if not os.path.exists("histo_statistics"):
			os.makedirs("histo_statistics")


#############################################################
# uHTR tests
# Results of each test recorded in master_dict
#############################################################

	def ped_test(self):
		ped_settings = list(i-31 for i in xrange(63))
		ped_results={}
		ped_results["settings"]=ped_settings
		histo_slopes = [] #stores slopes for overall histogram
		for setting in ped_settings:
			print "testing pedestal setting", setting
			for qslot in self.qcards:
				dc=hw.getDChains(qslot, self.bus)
				dc.read()
				for chip in xrange(12):
					dc[chip].PedestalDAC(setting)
				dc.write()
				dc.read()
			histo_results=self.get_histo_results(self.crate, self.uhtr_slots)
			for uhtr_slot, uhtr_slot_results in histo_results.iteritems():
	                        for chip, chip_results in uhtr_slot_results.iteritems():
					key="{0}_{1}_{2}".format(uhtr_slot, chip_results["link"], chip_results["channel"])
					if setting == -31: ped_results[key]=[]
					ped_results[key].append(chip_results["pedBinMax"])

		#reset pedastals to default
		for qslot in self.qcards:
			dc=hw.getDChains(qslot, self.bus)
			dc.read()
			for chip in xrange(12):
				dc[chip].PedestalDAC(6)
			dc.write()
			dc.read()

		#analyze results and make graphs
		cwd=os.getcwd()
		if not os.path.exists("ped_plots"):
			os.makedirs("ped_plots")
		os.chdir(cwd  + "/ped_plots")
		
		for qslot in self.qcards:
			for chip in xrange(12):
				chip_map=self.get_QIE_map(qslot, chip)
				ped_key = "{0}_{1}_{2}".format(chip_map[0], chip_map[1], chip_map[2])
				chip_arr = ped_results[ped_key]
				
				#check if settings -31 to -3 are flat and -2 to 31 are linear
				flat_test = True
				slope_test = False
				results = False
				for num in xrange(28):
					if chip_arr[num] != 1: flat_test=False
				slope = graph_results(self.uHTR_log, "ped", ped_settings, chip_arr, "{0}_{1}".format(qslot, chip))
				if slope <= 2.4 and slope >=2.15: slope_test = True
				print "qslot: {0}, chip: {1}, slope: {2}, pass flat test: {3}, pass slope test: {4}".format(qslot, chip, slope, flat_test, slope_test)
				
				# update master_dict with test results
				if flat_test and slope_test: results=True
				self.update_QIE_results(qslot, chip, "ped", results)

				#update slopes for final histogram
				histo_slopes.append(slope)
		os.chdir(cwd)

		#make histogram of all slope results
		os.chdir(cwd + "/histo_statistics")	
		make_histo(self.uHTR_log, "ped", histo_slopes, 0, 5)
		os.chdir(cwd)



	def ci_test(self):
		ci_settings = [90, 180, 360, 720, 1440, 2880, 5760, 8640] #in fC
		ci_results={}
		ci_results["settings"]=ci_settings
		histo_slopes = [] #stores all slopes for overall histogram
		adc = hw.ADCConverter()

		for setting in ci_settings:
			print "testing charge injection setting {0} fC".format(setting)
			for qslot in self.qcards:
				hw.SetQInjMode(1, qslot, self.bus)
				dc=hw.getDChains(qslot, self.bus)
				dc.read()
				for chip in xrange(12):
					dc[chip].ChargeInjectDAC(setting)
				dc.write()
				dc.read()
			histo_results=self.get_histo_results(self.crate, self.uhtr_slots, signalOn=True, out_dir="ci_histos_{0}".format(setting))

			for uhtr_slot, uhtr_slot_results in histo_results.iteritems():
	                        for chip, chip_results in uhtr_slot_results.iteritems():
					key="{0}_{1}_{2}".format(uhtr_slot, chip_results["link"], chip_results["channel"])
					if setting == 90: ci_results[key]=[]
				       	if 'signalBinMax_1' in chip_results:
						totalSignal = adc.linearize(chip_results['signalBinMax_1'])
						if 'signalBinMax_2' in chip_results:	# get 2nd peak if needed
							totalSignal += adc.linearize(chip_results['signalBinMax_2'])
						ci_results[key].append(totalSignal)

		#Turn off charge injection
		for qslot in self.qcards:
			hw.SetQInjMode(0, qslot, self.bus)

		#analyze results and make graphs
		cwd=os.getcwd()
		if not os.path.exists("ci_plots"):
			os.makedirs("ci_plots")
		os.chdir(cwd  + "/ci_plots")
		for qslot in self.qcards:
			for chip in xrange(12):
				chip_map=self.get_QIE_map(qslot, chip)
				ci_key = "{0}_{1}_{2}".format(chip_map[0], chip_map[1], chip_map[2])
				chip_arr = ci_results[ci_key]
				slope = graph_results(self.uHTR_log, "ci", ci_settings, chip_arr, "{0}_{1}".format(qslot, chip))
				print "qslot: {0}, chip: {1}, slope: {2}".format(qslot, chip, slope)

				#update slopes for final histogram
				histo_slopes.append(slope)
		os.chdir(cwd)

		#make histogram of all slope results
		os.chdir(cwd + "/histo_statistics")	
		make_histo(self.uHTR_log, "ci", histo_slopes, 0, 2)
		os.chdir(cwd)


	def phase_test(self):
		phase_settings = xrange(128)
		phase_results={}
		phase_results["settings"]=phase_settings
		for setting in phase_settings:
			print "testing phase_test setting", setting
			for qslot in self.qcards:
				dc=hw.getDChains(qslot, self.bus)
				dc.read()
				for chip in xrange(12):
					dc[chip].PhaseDelay(setting)
				dc.write()
				dc.read()

			tdc_results=self.get_tdc_results(self.crate, self.uhtr_slots)
			for uhtr_slot, uhtr_slot_results in tdc_results.iteritems():
				for link, links in uhtr_slot_results.iteritems():
					for channel, chip_results in links.iteritems():
						for k in range(len(chip_results)):
							if chip_results[k] != 63 and chip_results[k] != 62 and chip_results[k] != 0:
								key="{0}_{1}_{2}".format(uhtr_slot, link, channel)
								if setting == 0: phase_results[key]=[]
								phase_results[key].append(chip_results[k])
								break
							if k == len(chip_results)-1:
								key="{0}_{1}_{2}".format(uhtr_slot, link, channel)
								if setting == 0: phase_results[key]=[]
								phase_results[key].append(chip_results[k])	
		#reset phases to default
		for qslot in self.qcards:
			dc=hw.getDChains(qslot, self.bus)
			dc.read()
			for chip in xrange(12):
				dc[chip].PhaseDelay(0)
			dc.write()
			dc.read()
		cwd=os.getcwd()
	       
		#analyze results and make graphs
		if not os.path.exists("phase_plots"):	
			os.makedirs("phase_plots")
		os.chdir(cwd  + "/phase_plots")
		for qslot in self.qcards:
			for chip in xrange(12):
				chip_map=self.get_QIE_map(qslot, chip)
				phase_key = "{0}_{1}_{2}".format(chip_map[0], chip_map[1], chip_map[2])
				chip_arr = phase_results[phase_key]
				slope = graph_results(phase_settings, chip_arr, "{0}_{1}".format(qslot, chip), "phase")
				print "qslot: {0}, chip: {1}, slope: {2}".format(qslot, chip, slope)
		os.chdir(cwd)

 
	def shunt_test(self):
		peak_results = {}
		default_peaks = [] #holds the CI values for 3.1 fC/LSB setting for chips
		grand_ratio_pf = [0,0] #check for troubleshooting
		default_peaks_avg = 0
		adc = hw.ADCConverter()
		
		setting_list = [3.1, 4.65, 6.2, 9.3, 12.4, 15.5, 18.6, 21.7, 24.8, 27.9, 31, 34.1, 35.65] # fC/LSB gains in GSel table
		gain_settings = [0, 1, 2, 4, 8, 16, 18, 20, 24, 26, 28, 30, 31]
		
		#ratio between default 3.1fC/LSB and itself/other GSel gains
		nominalGainRatios = [1.0, 0.667, 0.5, 0.333, 0.25, 0.2, 0.167, 0.143, 0.125, 0.111, 0.1, 0.091, 0.087]

		histo_ratios=[]
		for x in xrange(len(gain_settings)):
			histo_ratios.append(x)
			histo_ratios[x] = []
		
		for setting in gain_settings:
			print "testing shunt setting", setting
			for qslot in self.qcards:
				dc=hw.getDChains(qslot, self.bus)
				dc.read()
				hw.SetQInjMode(1, qslot, self.bus)    #turn on CI mode (igloo function)
				for chip in xrange(12):
					dc[chip].PedestalDAC(6)
					dc[chip].ChargeInjectDAC(8640)    #set max CI value
					dc[chip].Gsel(setting)    #increase shunt/decrease gain
				dc.write()
				dc.read()

			histo_results=self.get_histo_results(self.crate, self.uhtr_slots, signalOn=True, out_dir="shunt_histos_{0}".format(setting))

			for uhtr_slot, uhtr_slot_results in histo_results.iteritems():
				for chip, chip_results in uhtr_slot_results.iteritems():
					key="{0}_{1}_{2}".format(uhtr_slot, chip_results["link"], chip_results["channel"])
					if setting == 0: peak_results[key] = []
					if 'signalBinMax_1' in chip_results:
						totalSignal = adc.linearize(chip_results['signalBinMax_1'])
						if 'signalBinMax_2' in chip_results:	# get 2nd peak if needed
							totalSignal += adc.linearize(chip_results['signalBinMax_2'])
						peak_results[key].append(totalSignal)
						if setting == 0:
							default_peaks.append(totalSignal)

		# reset Gsel to zero
		for qslot in self.qcards:
			dc=hw.getDChains(qslot, self.bus)
			dc.read()
			for chip in xrange(12):
				dc[chip].Gsel(0) #set Gsel back to default
			dc.write()
			dc.read()

		# calculate average default CI peak of default shunt
		default_peaks_avg = sum(default_peaks)/len(default_peaks)

		for qslot in self.qcards:
			for chip in xrange(12):
				chip_map=self.get_QIE_map(qslot, chip)
				peak_key = "{0}_{1}_{2}".format(chip_map[0], chip_map[1], chip_map[2])
				chip_arr=peak_results[peak_key]

				for setting in xrange(len(peak_results[peak_key])):
					ratio = float(peak_results[peak_key][setting]) / default_peaks_avg     #ratio between shunt-adjusted peak & default peak
					histo_ratios[setting].append(ratio)
					if (ratio < nominalGainRatios[setting]*1.15 and ratio > nominalGainRatios[setting]*0.85):     #within 15% of nominal
						setting_result = True
						grand_ratio_pf[0]+=1
					else:
						setting_result = False
						grand_ratio_pf[1]+=1

					self.update_QIE_results(qslot, chip, "shunt", setting_result)

					print "qslot: {0}, chip: {1}, setting: {2}, ratio: {3}".format(qslot, chip, setting, ratio)
		
		# for trouble shooting, shouldn't be in final test
		print "Total Pass/Fail for Shunt Test:  ({0}, {1})".format(grand_ratio_pf[0], grand_ratio_pf[1])
		
		#make histogram of all results for each setting
		cwd = os.getcwd()
		os.chdir(cwd + "/histo_statistics")
		
		for i, setting in enumerate(setting_list):
			make_histo(self.uHTR_log, "shunt", histo_ratios[i], nominalGainRatios[i]*0.85, nominalGainRatios[i]*1.15, setting)
		
		os.chdir(cwd)

#############################################################


#############################################################
# Adding and extracting data from the master_dict
#############################################################

	def get_QIE(self, qslot, chip):
		### Returns the dictionary storing the test results of the specified QIE chip
		key="({0}, {1})".format(qslot, chip)
		return self.master_dict[key]

	def get_QIE_results(self, qslot, chip, test_key):
		### Returns the (pass, fail) tuple of specific test
		qie_results=self.get_QIE(qslot, chip)[test_key]
		return (qie_results[0], qie_results[1])

	def update_QIE_results(self, qslot, chip, test_key, results):
		#results so that True = pass and False = fail
		qie_results=self.get_QIE(qslot, chip)[test_key]
		if results: qie_results[0]+=1
		else: qie_results[1]+=1

	def get_QIE_map(self, qslot, chip):
		key="({0}, {1})".format(qslot, chip)
                qie=self.master_dict[key]
		uhtr_slot=qie["uhtr_slot"]
		link=qie["link"]
		channel=qie["channel"]
		return (uhtr_slot, link, channel)

	def add_QIE(self, qcard_slot, chip, uhtr_slot, link, channel):
		QIE_info={}
		QIE_info["uhtr_slot"]=uhtr_slot
		QIE_info["link"]=link
		QIE_info["channel"]=channel
		# test results stored in a pass fail list
		QIE_info["ped"]=[0,0]
		QIE_info["ci"]=[0,0]
		QIE_info["phase"]=[0,0]
		QIE_info["shunt"]=[0,0]
		key="({0}, {1})".format(qcard_slot, chip)
		self.master_dict[key]=QIE_info

#############################################################


#############################################################
# Mapping functions
#############################################################

	def QIE_mapping(self):
		# Records the uHTR slot, link, and channel of each QIE in master_dict
		failures=[]
		for qslot in self.qcards:
			print "mapping qslot", qslot
			dc=hw.getDChains(qslot, self.bus)
			hw.SetQInjMode(0, qslot, self.bus)
			dc.read()
			for chip in [0,6]:
				for num in xrange(12):
					dc[num].PedestalDAC(-9)
					if num==chip:
						dc[num].PedestalDAC(31)
				dc.write()
				dc.read()
				info=self.get_mapping_histo()
				if info is not None:
					uhtr_slot=info[0]
					link=info[1]
					for i in xrange(6):
						self.add_QIE(qslot, chip+i, uhtr_slot, link, 5-i)
				else:
					print "mapping qcard {0} failed".format(qslot)
					self.qcards.remove(qslot)
					failures.append(qslot)
			for num in xrange(12):
				dc[num].PedestalDAC(6)
				dc.write()
				dc.read()
		
		for failure in failures:
			self.qcards.remove(failure)

	def get_mapping_histo(self):
		# matches histo to QIE chip for mapping
		map_results=self.get_histo_results(out_dir="map_histos")
		for uhtr_slot, uhtr_slot_results in map_results.iteritems():
			for chip, chip_results in uhtr_slot_results.iteritems():
				if chip_results["pedBinMax"] > 15:
					return (int(uhtr_slot), chip_results["link"], chip_results["channel"])
		return None

#############################################################


#############################################################
# Generate and read histos
#############################################################

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
			slot_num = str(file.split('_')[-1].split('.root')[0])

			histo_results[slot_num] = getHistoInfo(signal=signalOn, file_in=path_to_root+"/"+file)
#		shutil.rmtree(out_dir)
		return histo_results

#############################################################


#############################################################
# Generate and read TDC txt 
#############################################################

	def get_tdc_results(self, crate=None, slots=None, outDir="tdctests"):

		if slots is None:
			slots=self.uhtr_slots
		if crate is None:
			crate=self.crate
		TDCInfo = {}
		path_to_txt = generate_tdcs(crate, slots, outDir=outDir)
		for file in os.listdir(path_to_txt):
			# Extract slot number from file name
			slotNum = str(file.split("_")[-1].split(".txt")[0])

			TDCInfo[slotNum] = getTDCInfo(inFile=path_to_txt+"/"+file)

		return TDCInfo

############################################################


#############################################################
# uHTRtool histo functions
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


def getHistoInfo(file_in="", sepCapID=False, signal=False, qieRange = 0):
	ROOT.gROOT.SetBatch()
	slot_result = {}
	f = ROOT.TFile(file_in, "READ")
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
					h.GetXaxis().SetRangeUser(0,35)
					binMax = h.GetMaximumBin()
					chip_results["pedBinMax"] = h.GetMaximumBin()
					chip_results["pedRMS"] = h.GetRMS()
					binValue = 0
					binNum = 0
					peakCount = 0
					for Bin in range(15, lastBin):
						if h.GetBinContent(Bin) >= binValue:
							binValue = h.GetBinContent(Bin)
							binNum = Bin
						elif binValue != 0 and h.GetBinContent(Bin) == 0:
							peakCount += 1
							chip_results["signalBinMax_%d"%(peakCount)] = binNum
							binValue = 0	
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

#############################################################


#############################################################
# uHTRtool spy functions
#############################################################

def generate_tdcs(crate, slots, outFileBase="", outDir="tdctests"):
	if not outFileBase:
		outFileBase = "uHTR_tdctest"
	cwd = os.getcwd()
	if not os.path.exists(outDir):
		os.makedirs(outDir)
	dirPath = "{0}/{1}".format(cwd, outDir)
	os.chdir(dirPath)

	for slot in slots:
		outFile = outFileBase + "_{0}_{1}.txt".format(crate, slot)
		process = mp.Process(target=get_tdc, args=(crate, slot, outFile))
		process.start()

	while mp.active_children():
		time.sleep(0.1)

	os.chdir(cwd)
	return dirPath

def getTDCInfo(inFile=""):
	
	linesList = [line.rstrip("\n") for line in open(inFile)]
	slotResult = defaultdict(dict)
	foundLink = 0
	for j in range(len(linesList)):
		if len(linesList[j].split(" Fiber ")) == 2:
			linkInfo = linesList[j].split(" Fiber ")[1].split(" ")
			Link = int(linkInfo[0])
			Channel = int(linkInfo[2])
			foundLink = 1
			if "%d"%(Channel) not in slotResult.get("%d"%(Link),{}):
				slotResult["%d"%(Link)]["%d"%(Channel)] = []
		elif len(linesList[j].split(" TDC ")) == 2 and foundLink != 0:
			TDCVal = linesList[j].split(" TDC ")[1].split(" SOI")[0]
			slotResult["%d"%(Link)]["%d"%(Channel)].append(int(TDCVal))
	return slotResult

def get_tdc(crate, slot, outFile=""):

	if not outFile:
		outFile = "tdc_uhtr{0}.txt".format(slot)

	spyCMDS = [
		   "0",
	           "DAQ",
		   "CTL",
 	  	   "21",
		   "3",
		   "10",
		   "-1",
		   "MULTISPY",
		   "10",
		   "{0}".format(outFile),
                   "QUIT",
		   "EXIT"
	]
	send_commands(crate=crate, slot=slot, cmds=spyCMDS)

#############################################################

#############################################################
#Initialization functions
#############################################################

def uHTRtool_source_test():
	        ### checks to see if the uHTRtool is sourced, and sources it if needed
		uhtr_cmd="uHTRtool.exe"
		error="sh: uHTRtool.exe: command not found"
		check=getoutput(uhtr_cmd)
		source_cmd=["source /home/daqowner/dist/etc/env.sh"]

		if check==error:
			print "WARNING, you need to run 'source ~daqowner/dist/etc/env.sh' before you can use uHTRtool.exe"


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


def init_links(crate, slot, attempts=0):
	if attempts == 10:
		print "Skipping initialization of links for crate %d, slot %d after 10 failed attempts!"%(crate,slot)
		return
	attempts += 1
	linkInfo = get_link_info(crate, slot)
	onLinks, goodLinks, badLinks = check_link_status(linkInfo)
	if onLinks == 0:
		print "All crate %d, slot %d links are OFF! NOT initializing that slot!"%(crate,slot)
		return
	if badLinks == 0:
		return
	medianOrbitDelay = int(median_orbit_delay(linkInfo))
	if badLinks > 0:
		initCMDS = ["0","link","init","1","%d"%(medianOrbitDelay),"0","0","0","quit","exit"]
		send_commands(crate=crate, slot=slot, cmds=initCMDS)
		init_links(crate, slot, attempts)


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
	BCNMedian = int(np.median(BCNList))
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

#############################################################
# Analyze test results
#############################################################

def graph_results(log, test, x, y, key):
	if len(x) != len(y):
		print "Sets are of unequal length"
		return None
	
	if test == "ped":
		title="Pedestal Test Results {0}".format(key)
		ytitle="Pedestal Bin Max (fC)"
		plot_base="ped_{0}".format(key)
		adc=hw.ADCConverter()
		for i, yi in enumerate(y):
			y[i]=adc.linearize(yi)
		fit=ROOT.TF1("fit", "[0] + [1]*x", -2, 31)

	if test == "ci":
		title="Charge Injection Test Results {0}".format(key)
		ytitle="Charge Injection Bin Max (fC)"
		plot_base="ci_{0}".format(key)
		fit=ROOT.TF1("fit", "[0] + [1]*x", 0, 0)			

	if test == "phase":
		print "hi"

	g = ROOT.TGraph()
	for i in xrange(len(x)):
		g.SetPoint(i, x[i], y[i])
	c = ROOT.TCanvas("c1","c1",800,800)
	c.cd()
	g.Draw("AP")

	g.SetMarkerStyle(22)
	ROOT.gROOT.SetStyle("Plain")
	g.SetTitle(title)
	g.GetXaxis().SetTitle("Setting")
	g.GetXaxis().CenterTitle()
	g.GetYaxis().SetTitle(ytitle)
	g.GetYaxis().CenterTitle()
	g.Fit("fit","QR")
	slope = g.GetFunction("fit").GetParameter(1)
	g.Draw("AP")
	c.Print("{0}.png".format(plot_base))
	return slope

def make_histo(log, test, data, xmin, xmax, shunt_setting=0):

	if test == "ped":
		title = 'Pedestal Bin Max Slope Distribution'
		legend_title = 'All Chips'
		xtitle = "Slope"
		ytitle = "Number of Chips"
		plot_base="ped_{0}".format(log)

	if test == "ci":
		title = 'Charge Injection Bin Max Slope Distribution'
		legend_title = 'All Chips'
		xtitle = "Slope"
		ytitle = "Number of Chips"
		plot_base="ci_{0}".format(log)


	if test == "phase":
		print "hi"

	if test == "shunt":
		title = 'Shunt Setting: {0} fC/LSB'.format(shunt_setting)
		legend_title = 'All Chips'
		xtitle = "Ratio (Shunted/Default)"
		ytitle = "Number of Chips"
		plot_base="shunt_{0}_{1}".format(shunt_setting, log)

	c = ROOT.TCanvas('c','c', 800,800)
	c.cd()
	hist = ROOT.TH1D(legend_title, title, 20, xmin, xmax)
	hist.GetXaxis().SetTitle(xtitle)
	hist.GetYaxis().SetTitle(ytitle)
	for datum in data:
	    hist.Fill(datum)
	hist.Draw()
	c.Print("{0}.png".format(plot_base))

