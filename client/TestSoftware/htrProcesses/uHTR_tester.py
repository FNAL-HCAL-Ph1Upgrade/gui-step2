#!/usr/bin/python

from   histo_reader import *
from   histo_generator import * 
import argparse
import os
import time

usage = 'usage: %prog [options]'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-c', '--crate'   , dest='crate'  , help='crate number'    , default=41        , type=int)
parser.add_argument('-s', '--slot'    , nargs='+'     , help='slot number'     , default=5         , type=int)
parser.add_argument('-n', '--norbit'  , dest='norbits', help='number of orbits', default=1000      , type=int)
parser.add_argument('-i', '--sepCapID', dest='capID'  , help='separate cap id' , default=0         , type=int)
parser.add_argument('-d', '--outDir'  , dest='outDir' , help='output directory', default="joshtest", type=str)
parser.add_argument('-g', '--signal'  , dest='signal' , help='toggle signal'   , default=0         , type=int)
arg = parser.parse_args()

# Map list of strings to list of integers
arg.slot = map(int, arg.slot)

uHTRtool_source_test()
#Root_source_test()
pathToRoot = histo_tests(arg.crate, arg.slot, n_orbits=arg.norbits, sepCapID=arg.capID, file_out_base="", new_dir=arg.outDir)
time.sleep(2)
print pathToRoot
print os.listdir(pathToRoot)
for file in os.listdir(pathToRoot): 
	infoDictionary = getHistoInfo(signal=arg.signal, file_in=pathToRoot+"/"+file)
        print "Im watching you!" 
        for i in infoDictionary:
                print i, infoDictionary[i]
