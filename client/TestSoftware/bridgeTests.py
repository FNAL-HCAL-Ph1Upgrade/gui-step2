# A file containing many different files for running tests
# on bridge registers

from Test import Test
import calculateOrbits as co
import helpers as h
import temp 

# NOTE: some tests not included here are
# -I2C_SELECT (Address 0x11)
# -Igloo2_FPGA_Control (Address 0x22)
# -ControlReg (Address 0x2A)
# -The last two orbit histos are not included, as their 
#  i2C addresses overlap with those of the 

class ID_string(Test):
	def testBody(self):
		self.criteria = "0 77 82 69 72"
		self.bus.write(self.address, [0x00])	
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class ID_string_cont(Test):
	def testBody(self):
		self.criteria = "0 103 100 114 66"
		self.bus.write(self.address, [0x01])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Ones(Test):
	def testBody(self):
		self.criteria = "0 255 255 255 255"
		self.bus.write(self.address, [0x08])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Zeroes(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x09])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class OnesZeroes(Test):
	def testBody(self):
		self.criteria = "0 170 170 170 170"
		self.bus.write(self.address, [0x0A])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Firmware_Ver(Test):
	def testBody(self):
		self.criteria = "0 64 17 14 1"
		self.bus.write(self.address, [0x04])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class statusCheck(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x10])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class Temperature(Test):
	def testBody(self):
		self.temp == -99.0
		self.bus.write(0x00, [0x06])
		self.bus.write(self.address,[0x11,0x05,0,0,0])
		self.bus.write(0x40,[0xf3])
		self.bus.sleep(300)
		self.bus.read(0x40,2)

		bigData=self.bus.sendBatch()[-1]
		data=bigData[4]
		data=int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		temp = (-46.85) + 175.72*(data)/(2**16)
		temp = round(temp,3)

		if (temp > 10 and temp < 45):
			return (True, temp)
		else:
			return (False, temp)

class TempPass(Test):
	def testBody(self):
		print '\n'
		self.tempThreshold = 45
		self.tempResult = temp.readManyTemps(self.address,5,"Temperature","nohold")

		if (self.tempResult >= self.tempThreshold):
			print 'Temperature '+str(self.tempResult)+' exceeds '+str(self.tempThreshold)+'! TempPass test failed!'
			return False
		else:
			print 'Temperature: '+str(self.tempResult)+' in safe range!'
			return True

class HumiPass(Test):
	def testBody(self):
		print '\n'
		self.humiThreshold = 55
		self.humiResult = temp.readManyTemps(self.address,5,"Humidity","nohold")

		if (self.humiResult >= self.humiThreshold):
			print 'Humidity '+str(self.humiResult)+' exceeds '+str(self.humiThreshold)+'! HumiPass test failed!'
			return False
		else:
			print 'Humidity: '+str(self.humiResult)+' in safe range!'
			return True


class Humidity(Test):
	def testBody(self):
		humid = -99.0
		self.bus.write(0x00,[0x06])
		self.bus.write(qieCard,[0x11,0x05,0,0,0])
		self.bus.write(0x40,[0xf5])
		self.bus.sleep(500)
		self.bus.read(0x40,2)

		bigData = self.bus.sendBatch()[-1]
		data = bigData[4]
		data = int((hex(int(data.split()[0])))[2:] + (hex(int(data.split()[1])))[2:],16)
		#Converting the humidity using equation
		humid = -6 + 125.0*(data)/(2**16)
		humid = round(humid,3)

		if (humid > 0 and humid < 100):
			return True
		else:
			return False

class ScratchCheck(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x0B])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class brdg_ClockCounter(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x12])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class RES_QIE_Counter(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x13])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class WTE_Counter(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x14])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class ControlReg(Test):
	def testBody(self):
		self.criteria = "0 0 0 0 0"
		self.bus.write(self.address, [0x18])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		else: 
			return False

class OrbHist_5(Test):
	def testBody(self):
		return co.calcOrbs(self.bus,self.address,0.5,0)

class zeroOrbits(Test):
	def testBody(self):
		# Check for zeros for all oribts but [71:48] (bin 3 of 7)
		# This nonzero bin is address 0x1D
		zeroOrbitRegisters = [0x19,0x1A,0x1B,0x1C,0x1E,0x1F]
		for orbitReg in zeroOrbitRegisters:
			self.bus.write(self.address, [orbitReg])
			self.bus.read(self.address, 3)
			raw_data = self.bus.sendBatch()[-1]
			cooked_data = h.reverseBytes(raw_data)
			cooked_data = h.getValue(cooked_data)
			if (cooked_data != 0):
				print 'Nonzero orbit error!'
				return False
		return True

