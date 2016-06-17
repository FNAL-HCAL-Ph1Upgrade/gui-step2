def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))

def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret

bytes = [3,4,9]
bitList = getBitsFromBytes(bytes)
print bitList

def cat(bitList, first, length):
	bitString = ""
	for i in bitList[first:(first+length)]:
		bitString = bitString + i
	return bitString
print cat(bitList,0,24)

