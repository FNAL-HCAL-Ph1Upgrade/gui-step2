desiredReg = 'HELLO'
desiredReg = raw_input("Enter cntrReg name (default = 'all'): ")
if desiredReg == '':
    print "empty string"
elif desiredReg == 'HELLO':
    print "dg " + desiredReg
else:
    print "dg " +desiredReg

# def getByteFromBits(bitList):
#     return int(''.join(bitList), 2)
#
# # give a list with bits (list size should be a multiple of 8), returns list of each formed byte
# def getBytesFromBits(bitList):
#     ret = []
#     for i in xrange(len(bitList)/8):
#         ret.append(getByteFromBits(bitList[i * 8: (i + 1) * 8]))
#     return ret
#
# # give a string, returns list of each bit from string
# def stringToBitList(stringOfBits):
#     list = []
#     for i in stringOfBits:
#             list.append(i)
#
#     return list
#
# settingList = []
# settingList = raw_input("Please enter a List: ")
# print "You entered", settingList
# #we want to see if it cuts off leading zeroes for things like [01] -> 1
#
# settingStr = ''.join(settingList)
#
# print "settingStr: ", settingStr
#
# #toWrite = getBytesFromBits(stringToBitList(settingStr))
