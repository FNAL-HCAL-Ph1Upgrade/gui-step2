import glueFunctions as g
from TestSoftware.uHTR import uHTR

b = g.webBus('pi6',0)

g.openChannel(21, b)
b.write(h.getCardAddress(slot),[0x11,0x03,0,0,0])

uhtr = uHTR(6,qcard_slots,b)


#-------------------------------------
for slot in qcard_slots:
    print '__________________________________________________'
    print '____________________Slot %d_______________________' %slot
    print '__________________________________________________'
    myDC = h.getDChains(slot,b)

    # i.turnOnCI()
    h.SetQInjMode(0, slot, b)
    myDC.read()
    print myDC[0]

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
