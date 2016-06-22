#Hardware.py
import sys
sys.append('../')
from client import webBus
from DChains import DChains
#MUX dict
  #Given JX, set MUXes
class Hardware:
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

    def openChannel(slot, piAddress):
        rmLoc = getReadoutSlot(slot)
        bus = webBus(piAddress,0)
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
    def getDChains(slot, piAddress):
        Hardware.openChannel(slot, piAddress)
        return DChains(getCardAddress(slot), webBus(piAddress))


#SetQInjMode(t)
