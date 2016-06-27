# titas.py

from client import webBus
import TestSoftware.Hardware as h
import iglooClass as i
from TestSoftware.uHTR import uHTR

qcard_slots = [18,21]

b = webBus("pi6",0)


#############################################################################
# ChargeInjectDAC #########################################################
#############################################################################

# chips = list of chips (0-11) to set internal CI value to
def setChargeInjectDAC(chips = ['all'], ci_charge):

    if chips == ['all']: chips = list(c for c in xrange(12))

    for slot in qcard_slots:
        print '__________________________________________________'
        print '____________________Slot %d_______________________' %slot
        print '__________________________________________________'

        myDC = h.getDChains(slot,b) # get the daisy chains from QIE card

        # h.SetQInjMode(0, slot, b) # set charge injection mode on/off

        myDC.read()
        # prints current QIE register settings
        for chip in xrange(12):
            print "########################## CHIP %d ############" %chip
            print myDC[chip]

        for num in xrange(12):
            for chip in xrange(12):
                myDC[chip].ChargeInjectDAC(8640)
                myDC[chip].PedastalDAC(-9)
                # myDC[chip].CapID0pedastal(0)
                if chip == num:
                    myDC[chip].PedastalDAC(31)

            myDC.write()
            myDC.read()

            info = uhtr.get_mapping_histo()
            if info is not None:
                print "Q_slot: {4} Qie: {3}, uhtr_slot: {0}, link {1}: channel: {2}".format(info[0],info[1],info[2],chip,slot)

        for chip in xrange(12):
            print "########################## CHIP %d ############" %chip
            print myDC[chip]
