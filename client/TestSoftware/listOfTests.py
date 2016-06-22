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
	"BkPln_1" : bt.BkPln_Spare_1(b,a,i), "BkPln_2" : bt.BkPln_Spare_2(b,a,i), "BkPln_3" : bt.BkPln_Spare_3(b,a,i),
	"OrbHist_1" : bt.OrbHist_1(b,a,i),"OrbHist_2" : bt.OrbHist_2(b,a,i), "OrbHist_3" : bt.OrbHist_3(b,a,i),
	"OrbHist_4" : bt.OrbHist_4(b,a,i), "OrbHist_5" : bt.OrbHist_5(b,a,i)
	}
	
	return registers

def initializeIglooList(b,a,i):
	iglooRegs = {"fpgaMajVer" : ic.fpgaMajVer(b,a,i), "fpgaMinVer" : ic.fpgaMinVer(b,a,i),
	"iglooOnes" : ic.ones(b,a,i), "fpgaTopOrBot" : ic.fpgaTopOrBottom(b,a,i),
	"statusReg" : ic.statusReg(b,a,i), "cntrRegDisplay" : ic.cntrRegDisplay(b,a,i),
	"clk_count" : ic.clk_count(b,a,i), "rst_QIE_count" : ic.rst_QIE_count(b,a,i),
	"igloo_wte_count" : ic.wte_count(b,a,i), "capIDErr_count" : ic.capIDErr_count(b,a,i),
	"inputSpy" : ic.inputSpy(b,a,i), "cntrRegChange" : ic.cntrRegChange(b,a,i)
	}
	
	return iglooRegs


def initializeVttxList(b,a,i):
	vttxRegs = {"vttxDisplay" : vc.VTTX_Display(b,a,i),
		"vttxRwrWithRestore" : vc.VTTX_RWR_withRestore(b,a,i)\
		}
	return vttxRegs
