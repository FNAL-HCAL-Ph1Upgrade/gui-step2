var = 900
mlist= [0,4,5.0]
f = open('file.txt','w')
f.write('Var is %d '%var)
f.write('And again it is {0} '.format(var))
f.write(str(mlist))

# import ROOT
#
# mylist = []
#
# for i in xrange(192):
#     if i%4 == 0: mylist.append(float(1.07))
#     elif i%7 == 0: mylist.append(float(0.98))
#     else: mylist.append(float(1.0))
#
# print mylist
#
# c = ROOT.TCanvas('c1','c1', 800,800)
# c.cd()
#
# # Fill a ROOT histogram from a NumPy array
# hist = ROOT.TH1D('All Chips', 'Shunt Setting: 1', 20, .90, 1.10)
# hist.GetXaxis().SetTitle("Ratio Value")
# hist.GetYaxis().SetTitle("Number of Chips")
# # fill_hist(hist, mylist)
# for i in mylist:
#     hist.Fill(i)
# hist.Draw()
#
# c.Print('myroot.png')
