# Run complete QIE Test Sweet

def getUniqueIDs(RMList):
    uniqueIDArray = range(4)
    # Iterate through RM 0, 1, 2, 3 (include desired RMs in list)
    for rm in RMList:
        idList = range(4)
        # Iterate through Slot 0, 1, 2, 3 (run for all 4 slots by default)
        for slot in range(4):
            idList[slot] = uniqueID(rm,slot)
        uniqueIDArray[rm] = idList
    return uniqueIDArray
