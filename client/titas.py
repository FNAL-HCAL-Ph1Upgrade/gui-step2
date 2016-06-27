# titas.py

##### Imports #####
from client import webBus
import TestSoftware.Hardware as h
import iglooClass as i
from TestSoftware.uHTR import uHTR


##### Global Vars #####
pi = "pi6" # 'pi5' or 'pi6' etc
b = webBus(pi,0) # 0 = low server verbosity
slots = [18,21] # list of active J slots

# NOTE: unfortunate legacy code: spelling is "pedAstal" (not pedEstal)



##### Functions ######

''' display QIE registers of both daisy chains of a QIE card'''
def printDaisyChain(daisyChain):
    daisyChain.read()
    print "############################"
    for chip in xrange(12):
        print "##### Chip %d #####" %chip
        print chip

    print "############################"


''' change pedestal values for all chips on all cards in 'slots' list '''
def setPedastalDAC(slots, pedastal_val):
    #pedastal = magnitude * 2 fC
    #takes magnitudes -31 to 31

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].PedastalDAC(pedastal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID0 for all chips/slots '''
def setCapID0pedastal(slots, pedastal_val):
    #pedastal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID0pedastal(pedastal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID1 for all chips/slots'''
def setCapID1pedastal(slots, pedastal_val):
    #pedastal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID1pedastal(pedastal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID2 for all chips/slots'''
def setCapID2pedastal(slots, pedastal_val):
    #pedastal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID2pedastal(pedastal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID3 for all chips/slots'''
def setCapID3pedastal(slots, pedastal_val):
    #pedastal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID3pedastal(pedastal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' turn fixed range mode ON, select range mode '''
def setFixRangeModeOn(slots, qieRange):
    #fixed range mode = 1, autorange mode = 0

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot, b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].FixRange(1) # turn fixed range ON
            dcs[chip].RangeSet(qieRange)

        dcs.write() # write the changes for both daisy chains


''' turn fixed range mode OFF, use autorange '''
def setFixRangeModeOff(slots):
    #fixed range mode = 1, autorange mode = 0

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot, b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].FixRange(0) # turn fixed range OFF

        dcs.write() # write the changes for both daisy chains


''' set internal charge injection level for all chips/slots '''
# currently non-functional
def setChargeInjectDAC(slots, charge_val):
        # charge_val is decimal in fC: 
        # 90   : (0,0,0),
        # 180  : (0,0,1),
        # 360  : (0,1,0),
        # 720  : (0,1,1),
        # 1440 : (1,0,0),
        # 2880 : (1,0,1),
        # 5760 : (1,1,0),
        # 8640 : (1,1,1)

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot, b) # the 2 daisy chains from one QIE card

        for chip in xrange(12): # all 12 chips
            dcs[chip].ChargeInjectDAC(charge_val)

        dcs.write() # write the changes for both daisy chains
