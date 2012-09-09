#!/usr/bin/python
"""
Script to check the files, tar them and then check the tar so it matches the original.
v. 28 apr 2010
"""

#########################################################################
# HEADER DECLARATIONS							#
#########################################################################

from __future__ import with_statement

# Import modules
import commands
import os
import sys
import threading
import datetime
import time
import shutil
import hashlib

# Test "global" variables
if len(sys.argv) != 3:
	print " "
	print "Incorrect number of arguments given."
	print "Call the program as: " + sys.argv[0] + " <dir where folder to tar is at> <name of folder to tar>"
	print " "
	print "Exiting program."
	print " "
	sys.exit()

# Place "global" variables in the namespace
working_dir = sys.argv[1]
tar_name = sys.argv[2]

#########################################################################
# Checks if the folder is present					#
#########################################################################

if os.path.exists(working_dir)==0:
	print "\n \n Could not find the directory" + working_dir
	print "  Check your settings and try again.\n"
	sys.exit(1)

#########################################################################
# FUNCTION DECLARATIONS							#
#########################################################################

# Implementation of Ticker class
# Creates a progress bar made of points to indicate that the script is working
class Ticker(threading.Thread):
    def __init__(self, msg):
	threading.Thread.__init__(self)
	self.msg = msg
	self.event = threading.Event()
    def __enter__(self):
	self.start()
    def __exit__(self, ex_type, ex_value, ex_traceback):
	self.event.set()
	self.join()
    def run(self):
	sys.stdout.write(self.msg)
	while not self.event.isSet():
	    sys.stdout.write(".")
	    sys.stdout.flush()
	    self.event.wait(1)


def getmd5(this_file):
	"""
	Get the MD5 hash for the file.
	"""
	f1 = file(this_file ,'rb')
	m = hashlib.md5()
	while True:
		t = f1.read(1024)
		if len(t) == 0: break
		m.update(t)
	return m.hexdigest()

def fileExists(f):
	try:
		file = open(f)
	except IOError:
		exists = 0
	else:
		exists = 1
	return exists
	
#########################################################################
# EXECUTE THE SCRIPT							#
#########################################################################

initial_dir = os.getcwd()

os.chdir(working_dir)


with Ticker("\n Creating tar file"):
	status, output = commands.getstatusoutput('tar -cvf ' + initial_dir + '/' + tar_name + '.tar ' + tar_name)
	if status != 0:
		print " Problem with file " + tar_name
		print output
		print " "
		print " Exiting program."
		os.chdir(initial_dir)
		if fileExists(tar_name + ".tar"):
			commands.getstatusoutput('rm ' + tar_name + '.tar')
		sys.exit(1)
	else:
		print "\n Tar file created.\n"


with Ticker("\n Extracting tar file to check the files"):
	#Go back to startup dir
	os.chdir(initial_dir)
	status, output = commands.getstatusoutput('tar -xvf ' + tar_name + '.tar')
	if status != 0:
		print " Problem with file " + tar_name
		print output
		print " "
		print " Exiting program."
		os.chdir(initial_dir)
		if fileExists(tar_name + ".tar"):
			commands.getstatusoutput('rm ' + tar_name + '.tar')
		sys.exit(1)
	else:
		print "\n Tar file extracted.\n"


with Ticker("\n Checking the files with the original"):
	ls = os.listdir(working_dir + '/' + tar_name + '/')
	for item in ls:
		filemd5_1 = getmd5(working_dir + '/' + tar_name + '/' + item)
		filemd5_2 = getmd5(tar_name + '/' + item)
		if filemd5_1 != filemd5_2:
			print " The MD5 hash of the file " + item + " does not match the original!"
			print " "
			print " Exiting program."
			os.chdir(initial_dir)
			if fileExists(tar_name + ".tar"):
				commands.getstatusoutput('rm ' + tar_name + '.tar')
			sys.exit(1)
	shutil.rmtree(initial_dir + '/' + tar_name)

process_date = datetime.datetime.now().strftime("\n\n Check completed\n  %d/%m/%Y at %I:%M %p\n")

print process_date

#Go back to startup dir
os.chdir(initial_dir)

#send file to Fortress
with Ticker("\n Sending the file to FORTRESS"):
	status, output = commands.getstatusoutput('scp ' + tar_name + '.tar lvillanu@fortress.rcac.purdue.edu:/archive/fortress/home/lvillanu/archives2010/')
	if status != 0:
		print " Problem tranfering the file " + tar_name + " to Fortress"
		print output
		print " "
		print " Exiting program."
		sys.exit(1)
	else:
		print "\n Tar file uploaded to Fortress.\n"
		print output

#exit clean
sys.exit(0)
