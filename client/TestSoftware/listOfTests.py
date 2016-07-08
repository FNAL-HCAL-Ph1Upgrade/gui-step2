# listOfTests.py

# This files contains different functions that simply initialize tests to be ran
# during the main QC phase. This file isn't 100% necessary to the functionality of
# the GUI, but it really goes a long way to keep "tests.py" neat and orderly.

# Each function creates instances of specific tests. The function names are
# pretty self-explanatory.

import client
import bridgeTests as bt
import vttxClass as vc
import iglooClass as ic

def initializeBridgeList(b,a,i):
	registers = {"ID_string" : bt.ID_string(b,a,i), "ID_string_cont" : bt.ID_string_cont(b,a,i),
    	"Ones" : bt.Ones(b,a,i), "Zeroes" : bt.Zeroes(b,a,i), "OnesZeroes" : bt.OnesZeroes(b,a,i),
    	"Firmware_Ver" : bt.Firmware_Ver(b,a,i), "Status" : bt.statusCheck(b,a,i),
	"Scratch" : bt.ScratchCheck(b,a,i), "ClockCnt" : bt.brdg_ClockCounter(b,a,i),
	"QIECount" : bt.RES_QIE_Counter(b,a,i), "WTECount" : bt.WTE_Counter(b,a,i),
	"zeroOrbits" : bt.zeroOrbits(b,a,i), "TempPass" : bt.TempPass(b,a,i), "HumiPass" : bt.HumiPass(b,a,i)
	}
	
	return registers

def initializeIglooList(b,a,i):
	iglooRegs = {"fpgaMajVer" : ic.fpgaMajVer(b,a,i), "fpgaMinVer" : ic.fpgaMinVer(b,a,i),
	"iglooOnes" : ic.ones(b,a,i), "fpgaTopOrBot" : ic.fpgaTopOrBottom(b,a,i), "iglooZeros" : ic.zeroes(b,a,i),
	"statusReg" : ic.statusReg(b,a,i), "cntrRegDisplay" : ic.cntrRegDisplay(b,a,i),
	"clk_count" : ic.clk_count(b,a,i), "rst_QIE_count" : ic.rst_QIE_count(b,a,i),
	"igloo_wte_count" : ic.wte_count(b,a,i), "capIDErr_count" : ic.capIDErr_count(b,a,i),
	"igloo_UID" : ic.uniqueID(b,a,i), "Igloo2_FPGA_Control" : ic.Igloo2_FPGA_Control(b,a,i),
	"CI_Mode_On" : ic.CI_Mode_On(b,a,i), "CI_Mode_Off" : ic.CI_Mode_Off(b,a,i),
	}
	
	return iglooRegs

def initializeLongTests(b,a,i):
	longTestRegs = {"inputSpy_512Reads" : ic.inputSpy_512Reads(b,a,i), "OrbitHistograms" : bt.OrbHist_5(b,a,i)}	
	return longTestRegs

def initializeVttxList_1(b,a,i):
	vttxRegs_1 = {"vttxDisplay_1" : vc.VTTX_Display(b,a,i),
		"vttxRwrWithRestore_1" : vc.VTTX_RWR_withRestore(b,a,i)\
		}
	return vttxRegs_1

def initializeVttxList_2(b,a,i):
	vttxRegs_2 = {"vttxDisplay_2" : vc.VTTX_Display(b,a,i),
		"vttxRwrWithRestore_2" : vc.VTTX_RWR_withRestore(b,a,i)\
		}
	return vttxRegs_2
