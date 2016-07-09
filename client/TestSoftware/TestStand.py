#TestStand.py

import RM
import sys
import uHTR
import timeStamp
import loggerClass as logClass
from datetime import datetime
sys.path.append('../')
from client import webBus

class TestStand:
    def __init__(self, activeSlots, summaryList, suiteSelection, piAddress, iterations, uHTR_slots, user, overwrite):
        '''Create a test stand object filled with necessary RMs, cards'''
	self.bus = webBus(piAddress, 0)
	self.suiteSelection = suiteSelection	
	self.iters = iterations
	self.uHTR_slots = uHTR_slots
	self.user = user
	self.filename = sys.stdout.name  # For loggerclass use
	self.backupStdout = sys.stdout
	self.overwrite = overwrite
	self.timeString = "{:%b%d%Y_%H%M%S}".format(datetime.now())

        self.activeSlots = activeSlots
        self.RMs = []

        RM4_active = []
        RM3_active = []
        RM2_active = []
        RM1_active = []
	
	# Split the memory locations for summaries up based on what
	# RM slot they correspond to.
	RM4_summaries = summaryList[0:4]
	RM3_summaries = summaryList[4:8]
	RM2_summaries = summaryList[8:12]
	RM1_summaries = summaryList[12:16]

        for slot in self.activeSlots:
            if slot in [2,3,4,5]:
                #RM4
                RM4_active.append(slot)
            elif slot in [7,8,9,10]:
                #RM3
                RM3_active.append(slot)
            elif slot in [18,19,20,21]:
                #RM2
                RM2_active.append(slot)
            elif slot in [23,24,25,26]:
                #RM1
                RM1_active.append(slot)

        #initialize RMs
	print '--- Determining which slots contain active cards ---\n'
        self.RMs.append(RM.RM(1, RM1_active, RM1_summaries, self.bus))
        self.RMs.append(RM.RM(2, RM2_active, RM2_summaries, self.bus))
        self.RMs.append(RM.RM(3, RM3_active, RM3_summaries, self.bus))
        self.RMs.append(RM.RM(4, RM4_active, RM4_summaries, self.bus))
	print '\n--- Slot determination finished. Beginning tests ---\n\n'

    def runAll(self):
	    for r in self.RMs:
		r.runAll(self.suiteSelection, self.iters)
	    # uHTR tests need to be ran here, instead of being ran further down the line.
	    if (self.suiteSelection in ["main","uhtr"]):

		sys.stdout = logClass.loggerSingleTest(self.filename, "mappingHTRs")
		print '\n-------------------------'
		print 'Running uHTR tests!'
		print '-------------------------'
		print 'DEBUG... Active Slots: '+str(self.activeSlots)
		self.uHTR_instance = uHTR.uHTR(self.uHTR_slots, self.activeSlots, self.bus, self.user, self.overwrite)
		mapReturn = sys.stdout.strReturn
		mapReturn = mapReturn.replace("\\n","\n")
		sys.stdout = self.backupStdout		
		
		sys.stdout = logClass.loggerSingleTest(self.filename, "pedTests")
		self.uHTR_instance.ped_test()
		pedReturn = sys.stdout.strReturn
		pedReturn = pedReturn.replace("\\n","\n")
		sys.stdout = self.backupStdout

		sys.stdout = logClass.loggerSingleTest(self.filename, "citTests")
		self.uHTR_instance.ci_test()
		citReturn = sys.stdout.strReturn
		citReturn = citReturn.replace("\\n","\n")
		sys.stdout = self.backupStdout

		sys.stdout = logClass.loggerSingleTest(self.filename, "shtTests")
		self.uHTR_instance.shunt_test()
		shtReturn = sys.stdout.strReturn
		shtReturn = shtReturn.replace("\\n","\n")
		sys.stdout = self.backupStdout

		sys.stdout = logClass.loggerSingleTest(self.filename, "phsTests")
		self.uHTR_instance.phase_test()
		phsReturn = sys.stdout.strReturn
		phsReturn = phsReturn.replace("\\n","\n")
		sys.stdout = self.backupStdout


		self.uHTR_instance.make_jsons(mapReturn, pedReturn, citReturn, shtReturn, phsReturn)
		timeStamp.timestamp_results(self.timeString)
		
    def runSingle(self, key):
        for r in self.RMs:
            r.runSingle(key)

    def __repr__(self):
        '''Object representation'''
        return "TestStand()"

    def __str__(self):
        '''Return string representation of object data'''
        s = ""
        for i in xrange(len(self.RMs)):
            s += "RM%i:\n%s\n" % (i, str(self.RMs[i]))
        return s
