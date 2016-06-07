# Run complete QIE Test Sweet
from client import webBus
import uniqueID
b = webBus()
u = UniqueID

def run(RMList):
    uniqueIDArray = range(4)
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = range(4)
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in range(4):
            idList[slot] = u.uniqueID(rm,slot)
        uniqueIDArray[rm] = idList
    return uniqueIDArray

def printRun(RMList):
    uniqueIDArray = run(RMList)
    for rm in RMList:
        for slot in range(4):
            print 'RM: ', rm, ' slot: ', slot
            print 'UniqueID: ', uniqueIDArray[rm][slot]

printRun([0])
