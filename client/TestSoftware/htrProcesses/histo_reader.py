from ROOT import *
gROOT.SetBatch()

def getHistoInfo(file_in="", sepCapID=False, signal=False, qieRange = 0):
	result = {}
	f = TFile(file_in, "READ")
	if sepCapID:
		rangeADCoffset = qieRange*64.
		for i_link in range(24):
			for i_ch in range(6):
				histNum = 6*i_link + i_ch
				h = f.Get("h%d"%(histNum))
				info = {}
				info["link"] = i_link
				info["channel"] = i_ch
				info["binMax"] = []
				info["RMS"] = []
				for i_capID in range(4):
					offset = 64*(i_capID)
					h.GetXaxis().SetRangeUser(offset, offset+63)
					info["mean"].append(h.GetMean()-offset+rangeADCoffset)
					info["RMS"].append(max(h.GetRMS(), 0.01))

				result[histNum] = info
		
	else:
                if signal:
			for i_link in range(24):
				for i_ch in range(6):
					histNum = 6*i_link + i_ch
					h = f.Get("h%d"%(histNum))
					lastBin = h.GetSize() - 3
					info = {}
					info["link"] = i_link
					info["channel"] = i_ch
                                        #Transition from pedestal to signal is consistently around 10
                                        h.GetXaxis().SetRangeUser(7,13)
                                        cutoff = h.GetMinimum()
					h.GetXaxis().SetRangeUser(0,cutoff)
					binMax = h.GetMaximumBin()
					info["pedBinMax"] = h.GetBinContent(binMax) 
					info["pedRMS"] = h.GetRMS()
					h.GetXaxis().SetRangeUser(cutoff,lastBin)
					binMax = h.GetMaximumBin()
					info["signalBinMax"] = h.GetBinContent(binMax)
					info["signalRMS"] = h.GetRMS()

					result[histNum] = info

                else:
                        for i_link in range(24):
                                for i_ch in range(6):
                                        histNum = 6*i_link + i_ch
                                        h = f.Get("h%d"%(histNum))
                                        info = {}
                                       	info["link"] = i_link
					info["channel"] = i_ch
					info["pedBinMax"] = h.GetMaximumBin() 
					info["pedRMS"] = h.GetRMS()
					
                                        result[histNum] = info
 
	f.Close()
	return result
	
