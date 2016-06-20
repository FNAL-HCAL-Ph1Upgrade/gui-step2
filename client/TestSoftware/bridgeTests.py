# A file containing many different files for running tests
# on bridge registers

from Test import Test

# NOTE: some tests not included here are
# -I2C_SELECT (Address 0x11)
# -Igloo2_FPGA_Control (Address 0x22)
# -ControlReg (Address 0x2A)
# -The last two orbit histos are not included, as their 
#  i2C addresses overlap with those of the 

class ID_string(Test):
	def __init__(self):
		self.criteria = "0 77 82 69 72"

	def testBody(self):
		self.bus.write(self.address, [0x00])	
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class ID_string_cont(Test):
	def __init__(self):
		self.criteria = "0 77 82 69 72"

	def testBody(self):
		self.bus.write(self.address, [0x00])	
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False
		
class ID_string_cont(Test):
	def __init__(self):
		self.criteria = "0 103 100 114 66"

	def testBody(self):
		self.bus.write(self.address, [0x01])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Ones(Test):
	def __init__(self):
		self.criteria = "0 255 255 255 255"
	
	def testBody(self):
		self.bus.write(self.address, [0x08])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Zeroes(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x09])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class OnesZeroes(Test):
	def __init__(self):
		self.criteria = "0 170 170 170 170"

	def testBody(self):
		self.bus.write(self.address, [0x0A])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class Firmware_Ver(Test):
	def __init__(self):
		self.criteria = "0 0 0 11 01"
		
	def testBody(self):
		self.bus.write(self.address, [0x04])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria):
			return True
		else:
			return False

class statusCheck(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x10])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class Temperature(Test):
	def __init__(self):
		self.temp == -99.0
	
	def testBody(self)
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

class Humidity(Test):
	def __init__(self):
		humid = -99.0

	def testBody(self):
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
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x0B])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class brdg_ClockCounter(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x12])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class RES_QIE_Counter(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x13])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class WTE_Counter(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x14])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO
			return True
		else: 
			return False

class BkPln_Spare_1(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x15])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO, first char can't be 1
			return True
		else: 
			return False

class BkPln_Spare_2(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x16])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO, but first char can't be 1
			return True
		else: 
			return False

class BkPln_Spare_3(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x17])
		self.bus.read(self.address, 4)
		r=self.bus.sendBatch()[-1]
		if(r != self.criteria and r[0] != "1"): # Note we want NOT EQUAL TO, but first char can't be 1
			return True
		else: 
			return False

class orbit_histo_1(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x2B])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		else: 
			return False

class orbit_histo_2(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x2C])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		else: 
			return False

class orbit_histo_3(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x2D])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		else: 
			return False

class orbit_histo_4(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x2E])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		 Michéleelse: 
			return False

class orbit_histo_5(Test):
	def __init__(self):
		self.criteria = "0 0 0 0 0"

	def testBody(self):
		self.bus.write(self.address, [0x2F])
		self.bus.read(self.address, 3)
		r=self.bus.sendBatch()[-1]
		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
			return True
		else: 
			return False

#class orbit_histo_6(Test):
#	def __init__(self):
#		self.criteria = "0 0 0 0 0"
#
#	def testBody(self):
#		self.bus.write(self.address, [0x30])
#		self.bus.read(self.address, 3)
#		r=self.bus.sendBatch()[-1]
#		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
#			return True
#		else: 
#			return False
#
#class orbit_histo_7(Test):
#	def __init__(self):
#		self.criteria = "0 0 0 0 0"
#
#	def testBody(self):
#		self.bus.write(self.address, [0x31])
#		self.bus.read(self.address, 3)
#		r=self.bus.sendBatch()[-1]
#		if(r == self.criteria): # Note we want it to be equal to to the criteria string.
#			return True
#		else: 
#			return False
