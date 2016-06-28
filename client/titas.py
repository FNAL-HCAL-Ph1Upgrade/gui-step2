# All QIE register functions (i.e. TGain, CkOutEn, TDCmode, etc) can be found in QIE.py
# Daisy chain objects must use .read() after declaration (otherwise not instantiated completely, index goes out of range)
# Daisy chain objects must use .write() after changes are made in order to affect chips


##### Imports #####
from client import webBus
import TestSoftware.Hardware as h
# from TestSoftware.uHTR import uHTR


##### Global Vars #####
pi    = "pi6" # 'pi5' or 'pi6' etc
b     = webBus(pi,0) # webBus sets active pi; 0 = server verbosity off
slots = [18,21] # list of active J slots



##### Functions ######

''' display QIE registers of both daisy chains of a QIE card'''
def printDaisyChain(slots, bus):
    for i_slot in slots: # all desired slots
        ''' makes instance of daisy chain class for each card '''
        dcs = h.getDChains(i_slot, bus) # the 2 daisy chains from one QIE card

        dcs.read() # get real values for 2 daisy chains

        print "\n\n>>>>>>>>>>>> SLOT %d <<<<<<<<<<<<<" %i_slot

        for chip in xrange(12):
            print "\n######## CHIP %d ########" %chip
            print dcs[chip]

        print "############################"



''' change pedestal values for all chips on all cards in 'slots' list '''
def setPedestalDAC(slots, pedestal_val):
    #pedestal = magnitude * 2 fC
    #takes magnitudes -31 to 31

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].PedestalDAC(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID0 for all chips/slots '''
def setCapID0pedestal(slots, pedestal_val):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID0pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID1 for all chips/slots'''
def setCapID1pedestal(slots, pedestal_val):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID1pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID2 for all chips/slots'''
def setCapID2pedestal(slots, pedestal_val):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID2pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID3 for all chips/slots'''
def setCapID3pedestal(slots, pedestal_val):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID3pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' turn fixed range mode ON, select range mode '''
def setFixRangeModeOn(slots, qieRange, bus):
    #fixed range mode = 1, autorange mode = 0

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].FixRange(1) # turn fixed range ON
            dcs[chip].RangeSet(qieRange)

        dcs.write() # write the changes for both daisy chains


''' turn fixed range mode OFF, use autorange '''
def setFixRangeModeOff(slots, bus):
    #fixed range mode = 1, autorange mode = 0

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot, bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].FixRange(0) # turn fixed range OFF

        dcs.write() # write the changes for both daisy chains


''' set internal charge injection level for all chips/slots '''
# currently non-functional
def setChargeInjectDAC(slots, charge_val, bus):
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

        dcs = h.getDChains(i_slot, bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].ChargeInjectDAC(charge_val)

        dcs.write() # write the changes for both daisy chains


''' backplane reset (should be sent between I2C device selection)'''
def backplaneReset(bus):
    bus.write(0x00,[0x06])
    bus.sendBatch()


''' GPIO power enable via PCA9538 (address 0x70) (magic reset) '''
def powerEnable(bus):
    #Reset for ngccm 1 (for RM 2,1)
    for ngccm in [1,2]: #both ngccm
        bus.write(0x72,[ngccm])
        bus.write(0x74,[0x08]) # PCA9538 is bit 3 on ngccm mux
        bus.write(0x70,[0x03]) # GPIO PwrEn is register 3
        bus.read(0x70,1)
        batch = b.sendBatch()
        # print 'initial = ', batch

        message = batch[-1][2:]
        value = int(message) | 0x08
        bus.write(0x70,[0x03, value])
        bus.write(0x70,[0x03])
        bus.read(0x70,1)
        batch = bus.sendBatch()
        # print 'final = ', batch




##### Calling functions #####
powerEnable(b)
# printDaisyChain(slots,b)
# setPedastalDAC(slots,31,b)
# setCapID0pedastal(slots,0,b)
# setCapID1pedastal(slots,1,b)
# setCapID2pedastal(slots,1,b)
# setCapID3pedastal(slots,1,b)
# setFixRangeModeOn(slots,3,b)
# print "\n\n\n\n AFTER CHANGES: \n"
# printDaisyChain(slots,b)
