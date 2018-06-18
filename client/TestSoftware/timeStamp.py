from datetime import datetime
import os
import shutil

def timestamp_results(timestamp):
    cwd = os.getcwd()
    home = "/home/hep"
    tsdir = "{0}_Results".format(timestamp)
    dst = home + "/archivedResults/" + tsdir
    srcs = []
    src1 = "/jsonResults/"
#    src2 = "/logResults/"
    src3 = "/uhtrResults/"
    srcs.append(src1)
#    srcs.append(src2)
    srcs.append(src3)

    os.chdir(home)
    if not os.path.exists("archivedResults"):
        os.makedirs("archivedResults")
    os.chdir("archivedResults")

#    if not os.path.exists(tsdir):
#        os.makedirs(tsdir)
 
    os.chdir(home)
    
    for src in srcs:
        shutil.copytree(home+src, dst+src)

    for myFile in os.listdir('/home/hep/jsonResults/'):
		os.chdir('/home/hep/jsonResults/')
		os.remove(myFile)

    for myFile in os.listdir('/home/hep/uhtrResults/'):
		os.chdir('/home/hep/uhtrResults/')
		if os.path.isfile(myFile):
			os.remove(myFile)
		elif os.path.isdir(myFile):
			shutil.rmtree(myFile)
