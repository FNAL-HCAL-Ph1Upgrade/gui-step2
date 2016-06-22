#Hardware.py
import sys
sys.append('../')
from client import webBus
from DChains import DChains
#MUX dict
  #Given JX, set MUXes
class Hardware:
    cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]
    def getCardAddress(slot):
        if slot in [2,7,18,23] : return cardAddresses[0]
        if slot in [3,8,19,24] : return cardAddresses[1]
        if slot in [4,9,20,25] : return cardAddresses[2]
        if slot in [5,10,21,26]: return cardAddresses[3]

    def getReadoutSlot(slot):
        if slot in [2,3,4,5] : return     1
        if slot in [7,8,9,10] : return    2
        if slot in [18,19,20,21] : return 3
        if slot in [23,24,25,26] : return 4
    def ngccmGroup(rm):
        i2cGroups = [0x01, 0x10, 0x20, 0x02]
        return i2cGroups[rm-1]

    def openChannel(slot, bus):
        rmLoc = getReadoutSlot(slot)
        if rmLoc in [3,4]:
          # Open channel to ngCCM for RM 3,4: J1 - J10
            bus.write(0x72,[0x02])
        elif rmLoc in [1,2]:
          # Open channel to ngCCM for RM 1,2: J17 - J26
            bus.write(0x72,[0x01])
        else:
            print 'Invalid RM = ', rmLoc
            print 'Please choose RM = {1,2,3,4}'
            return 'closed channel'
      # Open channel to i2c group
        bus.write(0x74, [ngccmGroup(rmLoc)])
        bus.read(0x74, 2)
        return bus.sendBatch()

#Get DChains
    def getDChains(slot, bus):
        Hardware.openChannel(slot, bus)
        return DChains(getCardAddress(slot), bus)


#SetQInjMode(t)
    def SetQInjMode(onOffBit, slot, bus):
        openChannel(slot, bus)
        #expects onOffBit of 0 or 1
        if onOffBit == 0 or onOffBit == 1:
            bus.write(getCardAddress(slot),[0x11,0x03,0,0,0])
            bus.write(0x09,[0x11,onOffBit,0,0,0])
            bus.sendBatch()
        else:
            print "INVALID INPUT IN SetQInjMode... doing nothing"
