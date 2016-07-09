from client import webBus
import collections
from Checksum import Check
bus = webBus("pi5",0)
#bus = webBus("pi6",0)

# binDataHappy = '0 01110000 00111100 10000011'
# intDataHappy = '0 112 60 131'
# value = 28732

# Set last two bits of LSB to 0 (these are status bits).
# message = '0 01100011 01010010 01100100'
# 0110'0011'0101'0000 = 25424.

# Trigger T measurement     hold master     1110'0011   0xE3
# Trigger RH measurement    hold master     1110'0101   0xE5
# Trigger T measurement     no hold master  1111'0011   0xF3
# Trigger RH measurement    no hold master  1111'0101   0xF5

def reverse(message):
    mlist = message.split()
    error = mlist.pop(0)
    mlist.reverse()
    return error + " " + " ".join(mlist)

def getValue(message):
    value = ''
    mList = message.split()
    mList = mList[1:-1]
    for byte in xrange(len(mList)):
        initialByte = bin(int(mList[byte]))[2:]
        length = len(initialByte)
        zeros = "".join(list('0' for i in xrange(8-length)))
        fullByte = zeros + initialByte
        value += fullByte
    value = value[:-2] + '00'
    return int(value,2)

def calcTemp(s):
    return -46.85 + 175.72 * s/2**16

def calcHumi(s):
    return -6 + 125.0 * s/2**16

def mean(myList):
    return float(sum(myList))/len(myList)

# triggerList = [0xE3,0xE5,0xF3,0xF5]
trigger = collections.OrderedDict()
trigger['tempHold'] = 0xE3
trigger['humiHold'] = 0xE5
trigger['tempNoHold'] = 0xF3
trigger['humiNoHold'] = 0xF5

triggerDict = {
    'Temperature' : {
        'hold' : 0xE3,
        'nohold' : 0xF3
    },
    'Humidity' : {
        'hold' : 0xE5,
        'nohold' : 0xF5
    }
}

function = {
    'Temperature' : calcTemp,
    'Humidity' : calcHumi
}

# We have used 0xF3 for nohold, which has worked for temp.

def readTempHumi(slot, num_bytes, key, hold, verbosity=0):
    bus.write(0x00,[0x06])
    bus.write(slot,[0x11,0x05,0,0,0])
    bus.write(0x40,[triggerDict[key][hold]])
    bus.read(0x40, num_bytes + 1) # also read checksum byte
    message = bus.sendBatch()[-1]

#    crc = cc.checkCRC(message,2)
    check = Check(message,1)
    crc = check.result

    value = getValue(message)

    if verbosity > 1:
        print 'message: '+str(message)
        print 'checksum: '+str(crc)
        print 'value: '+str(value)
    return [crc,function[key](value)]

def readManyTemps(slot,iterations,key,hold,verbosity=0):
    tempArray = []
    for i in xrange(iterations):
        tempList = readTempHumi(slot,2,key,hold,verbosity)
        if verbosity > 0:
            print tempList
        tempArray.append(tempList)
        if int(tempList[0]) != 0:
            print '~~~~~ ERROR for Test '+str(i)+' : '+str(tempList)
    transpose = zip(*tempArray)
    finalTempList = transpose[1]
    tempMin = min(finalTempList)
    tempMax = max(finalTempList)
    tempMean = mean(finalTempList)
    tempCounter = collections.Counter(finalTempList)
    tempModeList = tempCounter.most_common()

    return tempMean

def run(slot,iterations,verbosity=0):
    tempResults = {"Temperature" : -99, "Humidity" : -99}
    for key in triggerDict:
        hold = 'nohold'
        tempResults[key]=readManyTemps(slot,iterations,key,hold,verbosity)
    return tempResults
	
