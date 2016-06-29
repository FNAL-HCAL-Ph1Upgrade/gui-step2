#!/usr/bin/env python

import numpy
from uHTR import send_commands

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
	
	print onLinks, goodLinks, badLinks
	print linkInfo["ON Status"] 
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

stuff = init_links(41, 6)

