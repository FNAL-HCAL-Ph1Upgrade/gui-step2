# Run complete QIE Test Sweet
from client import webBus
import uniqueID
b = webBus("pi5")
u = uniqueID

def run(RMList, num_slots):
    uniqueIDArray = range(4)
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = range(num_slots)
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in range(num_slots):
            idList[slot] = u.uniqueID(rm,slot)
            # b.clearBus()
        uniqueIDArray[rm] = idList
    return uniqueIDArray

def printRun(RMList, num_slots):
    uniqueIDArray = run(RMList, num_slots)
    for rm in RMList:
        for slot in range(num_slots):
            print 'RM: ', rm, ' slot: ', slot
            print 'UniqueID: ', uniqueIDArray[rm][slot]

# print u.openChannel(3,3)
printRun([0], 1)

# That output, though? It's Greek to me!
