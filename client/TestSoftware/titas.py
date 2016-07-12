# All QIE register functions (i.e. TGain, CkOutEn, TDCmode, etc) can be found in QIE.py
# Daisy chain objects must use .read() after declaration (otherwise not instantiated completely, index goes out of range)
# Daisy chain objects must use .write() after changes are made in order to affect chips


##### Imports #####
import sys
sys.path.append("../")
from client import webBus
import Hardware as h
import iglooClass_adry as i
from uniqueID import ID
# from uHTR import uHTR


##### Global Vars #####
pi    = "pi5" # 'pi5' or 'pi6' etc
b     = webBus(pi,0) # webBus sets active pi; 0 = server verbosity off
all_slots = [2,3,4,5,7,8,9,10,18,19,20,21,23,24,25,26]
slots = all_slots # list of active J slots

##### Functions ######

def chargeInjectOn(slots, bus):
    for slot in slots:
        h.SetQInjMode(1, slot, b)
        i.displayCI(bus,slot)

def chargeInjectOff(slots, bus):
    for slot in slots:
        h.SetQInjMode(0, slot, b)
        i.displayCI(bus,slot)

''' display QIE registers of both daisy chains of a QIE card'''
def printDaisyChain(slots, bus):
    for i_slot in slots: # all desired slots
        ''' makes instance of daisy chain class for each card '''
        dcs = h.getDChains(i_slot, bus) # the 2 daisy chains from one QIE card

        dcs.read() # get real values for 2 daisy chains

        print '\n\n>>>>>>>>>>>> SLOT %d <<<<<<<<<<<<<' %i_slot

        for chip in xrange(12):
            print '\n######## CHIP %d ########' %chip
            print dcs[chip]

        print '############################'


''' change tdc threshold '''
def setTimingThresholdDAC(slots, threshold_val, bus):

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].TimingThresholdDAC(threshold_val) # change threshold

        dcs.write() # write the changes for both daisy chains


''' change tdc threshold '''
def setTimingThresholdDAC(slots, threshold_val, bus):

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].TimingThresholdDAC(threshold_val) # change threshold

        dcs.write() # write the changes for both daisy chains



''' change pedestal values for all chips on all cards in 'slots' list '''
def setPedestalDAC(slots, pedestal_val, bus):
    #pedestal = magnitude * 2 fC
    #takes magnitudes -31 to 31

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].PedestalDAC(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID0 for all chips/slots '''
def setCapID0pedestal(slots, pedestal_val, bus):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID0pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID1 for all chips/slots'''
def setCapID1pedestal(slots, pedestal_val,bus):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID1pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID2 for all chips/slots'''
def setCapID2pedestal(slots, pedestal_val, bus):
    #pedestal = magnitude * ~1.9 fC
    #takes magnitudes -12 to 12

    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].CapID2pedestal(pedestal_val) # change pedestal

        dcs.write() # write the changes for both daisy chains


''' change pedestal for capID3 for all chips/slots'''
def setCapID3pedestal(slots, pedestal_val, bus):
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


''' change Gsel value '''
def setGsel(slots, gsel_val, bus):
    # valid gsel_val: 0,1,2,4,8,16,18,20,24
    # corresponds to 3.1, 4.65, 6.2, 9.3, 12.4, 15.5, 18.6, 21.7, 24.8 fC/LSB gain
    for i_slot in slots: # all desired slots

        dcs = h.getDChains(i_slot,bus) # the 2 daisy chains from one QIE card
        dcs.read()

        for chip in xrange(12): # all 12 chips
            dcs[chip].Gsel(gsel_val) # change gain

        dcs.write() # write the changes for both daisy chains


''' backplane reset (should be sent between I2C device selection)'''
def backplaneReset(bus):
    bus.write(0x00,[0x06])
    bus.sendBatch()


''' GPIO power enable via PCA9538 (address 0x70) (magic reset) '''
def powerEnable(bus):
    for ngccm in [1,2]: #both ngccm
        bus.write(0x72,[ngccm])
        bus.write(0x74,[0x08]) # PCA9538 is bit 3 on ngccm mux

        #power on and toggle reset
        bus.write(0x70,[0x03,0x00]) # Register 3 sets all GPIO pins to 'output' mode
        bus.write(0x70,[0x01,0x08]) # GPIO PwrEn is 0x08
        bus.write(0x70,[0x01,0x18]) # GPIO reset is 0x10
        bus.write(0x70,[0x01,0x08])

        #jtag selectors for slot 26
        # bus.write(0x70,[0x01,0x4A])

        bus.sendBatch()

##### Unique ID #####
# Initial with a buss and slot
def printID(bus, slots):
    for slot in slots:
        uID = ID(bus, slot)
        print '\nSlot J' + str(slot)
        print 'raw id = '+str(uID.raw+
        print 'serial id = '+str(uID.serial)
        print 'full id = '+str(uID.full+
        print 'really full id = '+str(uID.reallyfull)
        print 'split id = '+str(uID.split)
        print 'flip id = '+str(uID.flip)
        print 'sort id = '+str(uID.sort)

##### Calling functions #####

# powerEnable(b)
# chargeInjectOn(slots,b)
# #chargeInjectOff(slots,b)
# printDaisyChain(slots,b)
# setPedestalDAC(slots,6,b) #6bits->12fc is default
# #setCapID0pedestal(slots,0,b)
# # setCapID1pedestal(slots,1,b)
# # setCapID2pedestal(slots,1,b)
# # setCapID3pedestal(slots,1,b)
# # setFixRangeModeOn(slots,3,b)
# setChargeInjectDAC(slots,2880,b)
# print '\n\n\n\n\n AFTER CHANGES: \n'
# printDaisyChain(slots,b)

# Print ID given bus and slots
# printID(bus, slots)
# mySlots = [2,5,7,8,10]
printID(b,slots)

# print 'open = ', h.openChannel(2,b)
# print 'power = ', h.powerEnable(2,b)
# print 'reset = ', h.magicReset(2,b)
#
# print 'open = ', h.openChannel(18,b)
# print 'power = ', h.powerEnable(1,b)
# print 'reset = ', h.magicReset(1,b)
