# uses uHTRs for QIE tests 

import os
import sys
import time 
import multiprocessing as mp
from subprocess import Popen, PIPE
from commands import getoutput


def send_commands(crate=None, slot=None, cmds=''):
	# Sends commands to "uHTRtool.exe" and returns the raw output and a log. The input is the crate number, slot number, and a list of commands.
	# Arguments and variables:
	raw = ""
	results = {}                # Results will be indexed by uHTR IP unless a "ts" has been specified, in which case they'll be indexed by (crate, slot).

	## Parse cmds:
	if isinstance(cmds, str):
		print 'WARNING (uhtr.send_commands): You probably didn\'t intend to run "uHTRtool.exe" with only one command: {0}'.format(cmds)
		cmds = [cmds]

	# Prepare ip address:uhtr_ip = "192.168.%i.%i"%(crate, slot*4)
	uhtr_ip = "192.168.%i.%i"%(crate, slot*4)

	# Prepare the uHTRtool arguments:
	uhtr_cmd = "uHTRtool.exe {0}".format(uhtr_ip)   

	# Send commands and organize results:
	# This puts the output of the command into a list called "raw_output" the first element of the list is stdout, the second is stderr.
	raw_output = Popen(['printf "{0}" | {1}'.format(' '.join(cmds), uhtr_cmd)], shell = True, stdout = PIPE, stderr = PIPE).communicate()
	raw += raw_output[0] + raw_output[1]
	results[uhtr_ip] = raw
	return results

def uHTRtool_source_test():
	### checks to see if the uHTRtool is sourced, and sources it if needed	
	uhtr_cmd="uHTRtool.exe"
	error="sh: uHTRtool.exe: command not found"
	check=getoutput(uhtr_cmd)
	source_cmd=["source /home/daqowner/dist/etc/env.sh"]

	if check==error:
		print "WARNING, you need to run 'source ~daqowner/dist/etc/env.sh' before you can use uHTRtool.exe"

	return None

def get_histo(crate, slot, n_orbits=5000, sepCapID=0, file_out=""):
        # Set up some variables:
        log = ""
        if not file_out:
                file_out = "histo_uhtr{0}.root".format(slot)

        # Histogram:
        cmds = [
                '0',
                'link',
                'histo',
                'integrate',
                '{0}'.format(n_orbits),                # number of orbits to integrate over
                '{0}'.format(sepCapID),
                '{0}'.format(file_out),
                '0',
                'quit',
                'quit',
                'exit',
                '-1'
        ]
        result = send_commands(crate=crate, slot=slot, cmds=cmds)
        return result
	
def generate_histos(crates, slots, n_orbits=5000, sepCapID=0, file_out_base="", out_dir="histotests"):

	###check for single crate/single slot	
	if isinstance(crates, int):
		crates=[crates]

	if isinstance(slots, int):
		slots=[slots] 
	
	if not file_out_base:
		file_out_base="uHTR_histotest"

	cwd=os.getcwd()

	### check to see if out_dir exists and set it up if it does
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	dir_path="{0}/{1}".format(cwd, out_dir)
	os.chdir(dir_path)

	for crate in crates:
		for slot in slots:
			file_out=file_out_base+"_{0}_{1}.root".format(crate, slot)
			p = mp.Process(target=get_histo, args=(crate, slot, n_orbits, sepCapID, file_out,))
			p.start()

	while mp.active_children():
		time.sleep(0.1)

	print "All tests complete"	
			
	os.chdir(cwd)	

	### return the the full path to out_dir
	return dir_path

if __name__=="__main__": 
	slots=[1, 2, 3, 4, 5]
	generate_histos(41, slots)


