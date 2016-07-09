def getBitsFromByte(decimal):
    return list('%08d' % int(bin(decimal)[2:]))

def getBitsFromBytes(decimalBytes):
    ret = []
    for i in decimalBytes:
        ret = ret + getBitsFromByte(i)
    return ret

bytes = [3,4,9]
bitList = getBitsFromBytes(bytes)
#print bitList

def cat(bitList, first, length):
	bitString = ""
	for i in bitList[first:(first+length)]:
		bitString = bitString + i
	return bitString
#print cat(bitList,0,24)

data = '0000111110001001'
list = []
def convert(data):
	for i in data:
		list.append(i)
	return list

def getByteFromBits(bitList):
	return int(''.join(bitList),2)

def getBytesFromBits(bitList):
	ret = []
	for i in xrange(len(bitList)/8):
		ret.append(getByteFromBits(bitList[i*8 : (i+1) * 8]))
	return ret

#newList = convert(data)
#print 'newList: '+str(newList)
#print 'final result: '+str(getBytesFromBits(newList))

var = raw_input("Please enter a list: ")
print 'You entered'+str(var)
