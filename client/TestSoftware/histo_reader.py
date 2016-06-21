from ROOT import *
gROOT.SetBatch()

def getHistoInfo(file_in="", sepCapID=False, signal=False, qieRange = 0):
	slot_result = {}
	f = TFile(file_in, "READ")
	if sepCapID:
		rangeADCoffset = qieRange*64.
		for i_link in range(24):
			for i_ch in range(6):
				histNum = 6*i_link + i_ch
				h = f.Get("h%d"%(histNum))
				chip_results = {}
				chip_results["link"] = i_link
				chip_results["channel"] = i_ch
				chip_results["binMax"] = []
				chip_results["RMS"] = []
				for i_capID in range(4):
					offset = 64*(i_capID)
					h.GetXaxis().SetRangeUser(offset, offset+63)
					chip_results["RMS"].append(max(h.GetRMS(), 0.01))

				slot_result[histNum] = chip_results
		
	else:
                if signal:
			for i_link in range(24):
				for i_ch in range(6):
					histNum = 6*i_link + i_ch
					h = f.Get("h%d"%(histNum))
					lastBin = h.GetSize() - 3
					chip_results = {}
					chip_results["link"] = i_link
					chip_results["channel"] = i_ch
                                        #Transition from pedestal to signal is consistently around 10
                                        h.GetXaxis().SetRangeUser(7,13)
                                        cutoff = h.GetMinimum()
					h.GetXaxis().SetRangeUser(0,cutoff)
					binMax = h.GetMaximumBin()
					chip_results["pedBinMax"] = h.GetBinContent(binMax) 
					chip_results["pedRMS"] = h.GetRMS()
					h.GetXaxis().SetRangeUser(cutoff,lastBin)
					binMax = h.GetMaximumBin()
					chip_results["signalBinMax"] = h.GetBinContent(binMax)
					chip_results["signalRMS"] = h.GetRMS()

					slot_result[histNum] = chip_results

                else:
                        for i_link in range(24):
                                for i_ch in range(6):
                                        histNum = 6*i_link + i_ch
                                        h = f.Get("h%d"%(histNum))
                                        chip_results = {}
                                       	chip_results["link"] = i_link
					chip_results["channel"] = i_ch
					chip_results["pedBinMax"] = h.GetMaximumBin() 
					chip_results["pedRMS"] = h.GetRMS()
					
                                        slot_result[histNum] = chip_results
 
	f.Close()
	return slot_result
	
