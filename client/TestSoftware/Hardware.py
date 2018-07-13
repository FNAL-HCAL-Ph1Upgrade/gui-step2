#Hardware.py
import sys
from DChains import DChains
import helpers as t
#MUX dict
  #Given JX, set MUXes

cardAddresses = [0x19, 0x1A, 0x1B, 0x1C]
def getCardAddress(slot):
    if slot in [2,7,18,23] : return cardAddresses[0]
    if slot in [3,8,19,24] : return cardAddresses[1]
    if slot in [4,9,20,25] : return cardAddresses[2]
    if slot in [5,10,21,26]: return cardAddresses[3]

def getReadoutSlot(slot):
    if slot in [2,3,4,5] : return     4
    if slot in [7,8,9,10] : return    3
    if slot in [18,19,20,21] : return 2
    if slot in [23,24,25,26] : return 1
def ngccmGroup(rm):
    i2cGroups = [0x01, 0x10, 0x20, 0x02]
    return i2cGroups[rm-1]

def openChannel(slot, bus, backplane = 0):
    #backplane can be 0 or 1
    rmLoc = getReadoutSlot(slot)
    rmnum = rmLoc + 4 * backplane
    if rmLoc in [1,2]:
      # Open channel to ngCCM for RM 1,2: J17 - J26
        bus.write(0x72,[0x01])
    elif rmLoc in [3,4]:
      # Open channel to ngCCM for RM 3,4: J1 - J10
        bus.write(0x72,[0x02])
    elif rmLoc in [5,6]:
      # Open channel to ngCCM for RM 3,4: J1 - J10
        bus.write(0x72,[0x03])
    elif rmLoc in [7,8]:
      # Open channel to ngCCM for RM 3,4: J1 - J10
        bus.write(0x72,[0x04])
    else:
        print 'Invalid RM = ', rmLoc
        print 'Please choose RM = {1,2,3,4}'
        return 'closed channel'

  # Reset the backplane
    bus.write(0x00,[0x06])
    return #bus.sendBatch()

#Get DChains
def getDChains(slot, bus):
    openChannel(slot, bus)
    return DChains(getCardAddress(slot), bus)

#SetQInjMode(t)
def SetQInjMode(onOffBit, slot, bus):
    openChannel(slot, bus)
    #expects onOffBit of 0 or 1
    if onOffBit == 0 or onOffBit == 1:
        bus.write(getCardAddress(slot),[0x11,0x03,0,0,0])
        bus.write(0x09,[0x11,onOffBit,0,0,0])
        #bus.sendBatch()
    else:
        print 'INVALID INPUT IN SetQInjMode... doing nothing'

# Cryptic Magic Reset on 0x70
def magicReset(ngccm,bus): #RM4,3->ngccm=2 -- RM2,1->ngccm=1
    bus.write(0x72,[ngccm])
    bus.write(0x74,[0x08])
    bus.write(0x70,[0x3,0x0]) # Set to Output

    # The proper way... only change the bit you want to change!
    bus.write(0x70,[0x1])
    bus.read(0x70,1)
    message = bus.sendBatch()[-1]
    value1 = int(message[2:])
    value2 = value1 | 0x10

    bus.write(0x70,[0x1,value2])
    bus.write(0x70,[0x1,value1])

    return bus.sendBatch()

# Power Enable on 0x70
def powerEnable(ngccm,bus):
    bus.write(0x72,[ngccm]) #RM4,3->ngccm=2 -- RM2,1->ngccm=1
    bus.write(0x74,[0x08])
    bus.write(0x70,[0x3,0x0]) # Set to Output

    # The proper way... only change the bit you want to change!
    bus.write(0x70,[0x1])
    bus.read(0x70,1)
    message = bus.sendBatch()[-1]
    value1 = int(message[2:])
    value2 = value1 | 0x8

    bus.write(0x70,[0x1,value2])

    return bus.sendBatch()


# Converts ADC to fC (Nate Chaverin's class)
class ADCConverter:
    # Bitmasks for 8-bit ADC input

    expMask = 192
    manMask = 63
    baseSensitivity = 3.1
    # Base charges for each subrange
    # Use array for which 0 ADC = 0 fC input charge
    inputCharge = [
        -1.6, 48.4, 172.4, 433.4, 606.4,
        517, 915, 1910, 3990, 5380,
        4780, 7960, 15900, 32600, 43700,
        38900, 64300, 128000, 261000, 350000
    ]

    #Defines the size of the ADC mantissa subranges
    adcBase = [0, 16, 36, 57, 64]

    # A class to convert ADC to fC
    fc = {}

    def __init__(self):
        # Loop over exponents, 0 - 3
        for exp in xrange(0, 4):
            # Loop over mantissas, 0 - 63
            for man in xrange(0, 64):
                subrange = -1
                # Find which subrange the mantissa is in
                for i in xrange(0, 4):
                    if man >= self.adcBase[i] and man < self.adcBase[i + 1]:
                        subrange = i

                if subrange == -1:
                    print 'Something has gone horribly wrong: subrange = -1 in ADCConverter from Hardware.py (line 131)!'

                # Sensitivity = 3.1 * 8^exp * 2^subrange
                sensitivity = self.baseSensitivity * 8.0**float(exp) * 2.0**subrange
                # Add sensitivity * (location in subrange) to base charge
                #fc[exp * 64 + man] = (inputCharge[exp * 5 + subrange] + ((man - adcBase[subrange])) * sensitivity) / gain;
                self.fc[exp * 64 + man] = self.inputCharge[exp * 5 + subrange] + ((man - self.adcBase[subrange]) + .5) * sensitivity

    def linearize(self, adc):
        if adc > 255: adc = 255
        return self.fc[int(adc)]

# ------------------------------------------------------------------------
class iglooPower:
    def __init__(self, slot, bus):
        self.address = getCardAddress(slot)
        self.bus = bus
        openChannel(slot, bus)
        # print self.testBody()
        self.testBody()

    def testBody(self):
        # print '~~ Begin Toggle Igloo Power Slave'
        control_address = 0x22
        message = self.readBridge(control_address,4)
        # print 'Igloo Control = '+str(message)

        ones_address = 0x02
        all_ones = '255 255 255 255'

        retval = False

        self.bus.write(0x00,[0x06])
        self.bus.sendBatch()

        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
        	retval = False
        # print 'Igloo Ones = '+str(register)

        # Turn Igloo Off
        # print 'Igloo Control = '+str(self.toggleIgloo())
        self.toggleIgloo()
        register = self.detectIglooError(ones_address, 4)
        if register[0] != '0':
        	retval = True
        # print 'Igloo Ones = '+str(register)

        # Turn Igloo On
        # print 'Igloo Control = '+str(self.toggleIgloo())
        self.toggleIgloo()
        register = self.readIgloo(ones_address, 4)
        if register != all_ones:
        	retval = False
        # print 'Igloo Ones = '+str(register)
        if retval:
            print '~~~ Toggle Igloo Power PASS'
        else:
            print '~~~ Toggle Igloo Power FAIL'
        return retval

    def toggleIgloo(self):
        iglooControl = 0x22
        message = self.readBridge(iglooControl,4)
        value = t.getValue(message)
        value = value ^ 0x400 # toggle igloo power!
        messageList = t.getMessageList(value,4)
        self.writeBridge(iglooControl,messageList)
        return self.readBridge(iglooControl,4)

    def writeBridge(self, regAddress, messageList):
    	self.bus.write(0x19, [regAddress]+messageList)
    	return self.bus.sendBatch()

    def readBridge(self, regAddress, num_bytes):
        self.bus.write(0x00,[0x06])
        self.bus.sendBatch()
        self.bus.write(0x19,[regAddress])
        self.bus.read(0x19, num_bytes)
        message = self.bus.sendBatch()[-1]
        # if message[0] != '0':
        #     print 'Bridge i2c error detected'
        return t.reverseBytes(message[2:])

    def readIgloo(self, regAddress, num_bytes):
    	self.bus.write(0x00,[0x06])
    	self.bus.write(self.address,[0x11,0x03,0,0,0])
    	self.bus.write(0x09,[regAddress])
    	self.bus.read(0x09, num_bytes)
    	message = self.bus.sendBatch()[-1]
    	# if message[0] != '0':
    	# 	print 'Igloo i2c error detected in readIgloo'
    	return t.reverseBytes(message[2:])

    def detectIglooError(self, regAddress, num_bytes):
    	self.bus.write(0x00,[0x06])
    	self.bus.write(self.address,[0x11,0x03,0,0,0])
    	self.bus.write(0x09,[regAddress])
    	self.bus.read(0x09, num_bytes)
    	message = self.bus.sendBatch()[-1]
    	# if message[0] != '0':
    	# 	print 'Igloo Power Off Confirmed.'
    	return message

def toggleIgloos(bus):
    powerSlots = [2,7,18,23]
    for ps in powerSlots:
        print 'Igloo Power Control Slot J'+str(ps)
        ip = iglooPower(ps, bus)
