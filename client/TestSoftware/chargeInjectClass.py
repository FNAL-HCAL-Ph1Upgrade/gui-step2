import sys
sys.path.append('../')
from client import webBus
import Hardware as h
import iglooClass as i
# from TestSoftware.uHTR import uHTR

qcard_slots = [2,5]

b = webBus("pi5",0)
# uhtr = uHTR(6,qcard_slots,b)

#-------------------------------------
for slot in qcard_slots:
    print '__________________________________________________'
    print '____________________Slot %d_______________________' %slot
    print '__________________________________________________'
    myDC = h.getDChains(slot,b)

    # i.turnOnCI()
    d
    myDC.read()
    print myDC[0]

    print '__________________________________________________'
    print '__________________________________________________'
    print '__________________________________________________'

    # for num in xrange(12):
    #     for chip in xrange(12):
    #         myDC[chip].ChargeInjectDAC(8640)
    #         myDC[chip].PedestalDAC(-9)
    #         # myDC[chip].CapID0pedestal(0)
    #         if chip == num:
    #             myDC[chip].PedestalDAC(31)

    for chip in xrange(12):
        # myDC[chip].ChargeInjectDAC(8640)
        # myDC[chip].PedestalDAC(-9)


        myDC.write()
        myDC.read()

        info = uhtr.get_mapping_histo()
        if info is not None:
            print 'Q_slot: {4} Qie: {3}, uhtr_slot: {0}, link {1}: channel: {2}'.format(info[0],info[1],info[2],chip,slot)

    for chip in xrange(12):
        print '########################## CHIP %d ############' %chip
        print myDC[chip]

    i.displayCI(slot)
