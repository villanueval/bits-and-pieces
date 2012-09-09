#!/usr/bin/python
# v. 14 jun 08
"""
Generic script to trigger other scripts on a series of files.
This version does not copy the files from the server, it assumes
 the files are on the computer itself on /home/ljvillanueva/sounds
"""

#########################################################################
# HEADER DECLARATIONS							#
#########################################################################

from __future__ import with_statement

# Import modules
import commands
import os
import wave
import sys
import threading
import datetime
import time
import shutil

# Test "global" variables
if len(sys.argv) != 2:
	print " "
	print "Incorrect number of arguments given."
	print "Call the program as: " + sys.argv[0] + " <deployment_ID>"
	print " "
	print "Exiting program."
	print " "
	sys.exit()

# Place "global" variables in the namespace
deploymentID = sys.argv[1]

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

#Extract wav from FLAC
def extractflac(item):
	#Copy the FLAC from remote site to local
	#shutil.copyfile(working_dir + '/' + item, item)
	#Extract the wav from the flac
	#status, output = commands.getstatusoutput('flac -df ' + working_dir + '/' + item + ' -o ' + os.getcwd() + '/' + item[:-5] + '.wav')
	status, output = commands.getstatusoutput('flac -dFs ' + item)
	#Get filename with the .wav extention
	item_wav=item[:-5] + ".wav"
	if status != 0:
		print "Problem with file ", item[:-5]
		print "   The file is corrupted or not a FLAC file!!!"
		print output
		writelog(output)
		sys.exit()
	print "\nFile extract was successful"
	return item_wav

#Insert data to MySQL
def tomysql(item, deploymentID, filename, samprate, no_channels):
	status, output = commands.getstatusoutput('./wav2mysql.py ' + item + " " + deploymentID + " " + filename + " " + `samprate` + " " + `no_channels`)
	if status != 0:
		print " "
		print "There was a problem processing " + item + "!"
		print output
		sys.exit()
	else:
		print output
	print "\nMySQL Insert was successful"
	return

#Draw Waveform and Spectrogram to png files
def draw_png(item, itemname):
	status, output = commands.getstatusoutput('./wav2png.py -w 1000 -h 400 -f 4096 -m 11025 ' + `item` + ' -a ' + `itemname[:-4]` + '_w.png -s ' + `itemname[:-4]` + '_s.png')
	if status != 0:
		print " "
		print "There was a problem processing " + item + "!"
		print output
		sys.exit()
	print "\nPNG files creation was successful"
	return

#Make MP3 files using lame
def makemp3(item):
	#Convert wav to mp3
	status, output = commands.getstatusoutput('lame -h -b 128 ' + item + " " + item[:-4] + '.mp3')
	if status != 0:
		print "Problem with file "
		print output
		sys.exit()
	print "\nMP3 creation was successful"
	return

#Convert to 44.1 kHz
def make441(item):
	item2 = "temp.wav"
	status, output = commands.getstatusoutput('sox ' + item + ' -r 44100 ' + item2)
	if status != 0:
		print "Problem with file "
		print output
		sys.exit()
	#Rename to mantain original filename
	status, output = commands.getstatusoutput('rm ' + item)
	status, output = commands.getstatusoutput('mv ' + item2 + ' ' + item)
	if status != 0:
		print "Problem with file "
		print output
		sys.exit()
	print "\nSox processing successful"
	return item

def cleanup(working_dir,pngmp3_dir,deploymentID,item):
#	pathToDep = "/var/www/sounds/" + deploymentID
#	pathToDep = deploymentID
#	pathToPNG = pathToDep + "/png"
#	pathToMP3 = pathToDep + "/mp3"
	pathToDep = pngmp3_dir + deploymentID
	pathToPNG = pngmp3_dir + deploymentID + "/png"
	pathToMP3 = pngmp3_dir + deploymentID + "/mp3"
	pathToDone = working_dir + "/done"
	if os.path.exists(pathToDep)==0:
		status, output = commands.getstatusoutput('mkdir ' + pathToDep)
		if status != 0:
			print output
			sys.exit()
	if os.path.exists(pathToPNG)==0:
		status, output = commands.getstatusoutput('mkdir ' + pathToPNG)
		if status != 0:
			print output
                       	sys.exit()
	if os.path.exists(pathToMP3)==0:
		status, output = commands.getstatusoutput('mkdir ' + pathToMP3)
		if status != 0:
			print output
                       	sys.exit()
	if os.path.exists(pathToDone)==0:
		status, output = commands.getstatusoutput('mkdir ' + pathToDone)
		if status != 0:
			print output
                       	sys.exit()
	status, output = commands.getstatusoutput('rm -f *.flac')
	if status != 0:
		print output
		sys.exit()
	status, output = commands.getstatusoutput('rm -f *.wav')
	if status != 0:
		print output
		sys.exit()
	status, output = commands.getstatusoutput('mv *.png ' + pathToPNG)
	if status != 0:
		print output
		sys.exit()
	status, output = commands.getstatusoutput('mv *.mp3 ' + pathToMP3)
	if status != 0:
		print output
		sys.exit()
	#Move the already processed file to a done folder
	status, output = commands.getstatusoutput('mv ' + working_dir + '/' + item + ' ' + pathToDone + '/')
	if status != 0:
		print output
		sys.exit()
	return

def fileExists(f):
	try:
		file = open(f)
	except IOError:
		exists = 0
	else:
		exists = 1
	return exists

def checkifstereo(wave_file):
	"""
	Open the wave file specified in the command line or elsewhere for processing.
	"""
	wave_pointer = wave.open(wave_file,'rb')
	#Check if stereo
	no_channels = wave_pointer.getnchannels()
	return no_channels

def stereo2mono(wave_file):
	"""
	Convert the stereo file to mono using Sox and default options
	"""
	#Check if sox is installed
	status, output = commands.getstatusoutput('sox')
	if output[-9:] == 'not found':
		print " "
		print "Sox is not installed!"
		print "Please install with: sudo apt-get install sox libsox*"
		print " "
		print "Exiting program."
		print " "
		sys.exit()
	#Get the stereo filename
	print " "
	print "Stereo file, will convert to mono."
	print " "
	mono_name = "mono.wav"
	with Ticker("  working..."):
		status, output = commands.getstatusoutput('sox ' + wave_file + ' -c 1 ' + mono_name)
		print " "
		if status != 0:
			print "Problem with file ", wave_file[:-4]
			print "   Could not be converted to mono:,"
			print output
			print " "
			print "Exiting program."
			sys.exit()
		else:
			print "Stereo to mono conversion completed.\n"
#		status, output = commands.getstatusoutput('rm -f ' + wave_file)
#		print output
#		status, output = commands.getstatusoutput('mv ' + mono_name + " " + wave_file)
#		if status != 0:
#		print output
#			sys.exit()
	return mono_name

def getsamprate(wave_file):
	wave_pointer = wave.open(wave_file,'rb')
	srate = wave_pointer.getframerate()
	return srate

def writelog(to_write):
	logfile = open ( 'log.txt', 'a' )
	logfile.write ( to_write + '\n' )
	logfile.close()


#########################################################################
# EXECUTE THE SCRIPT							#
#########################################################################

#Change working dir
base_dir = '/mnt/gak/Soundscape/Recordings/'
pngmp3_dir = '/mnt/gak/Soundscape/pngmp3/'
working_dir = base_dir + deploymentID

#check if directory has been processed
donefile = working_dir + '/done.txt'
if fileExists(donefile):
	print "\nERROR: It seems this directory has been processed already:"
	f = open (donefile)
	for line in f:
        	print line,
	f.close()
	sys.exit()

#Copy python file to working dir
#commands.getstatusoutput('cp *.py ' + working_dir)

#Change working dir to dir with files
#os.chdir(working_dir)

ls = os.listdir(working_dir)
for item in ls:
	if item[-5:] == ".flac" or item[-5:] == ".FLAC":
		print '\nExecuting script on ' + item

		#Copy the FLAC from remote site to local
		#The try is in case the CIFS is not responding, wait two minutes and try again
		with Ticker("  Copying file from server..."):
			try:
				shutil.copyfile(working_dir + '/' + item, item)
			except IOError, (errno, strerror):
				time.sleep(60)
				shutil.copyfile(working_dir + '/' + item, item)
		print " "

		with Ticker("  Extracting wav file from FLAC..."):
			item = extractflac(item)
		print " "

		#Check if 44.1 kHz
		samprate = getsamprate(item)
		if samprate != 44100:
			item = make441(item)

		#Check if stereo
		no_channels = checkifstereo(item)
		if no_channels == 2:
			itemm = stereo2mono(item)
			with Ticker("  Inserting the data to MySQL..."):
				tomysql(itemm, deploymentID, item, samprate, no_channels)
			print " "
			with Ticker("  Drawing waveform and spectrogram..."):
				draw_png(itemm, item)
			print " "
			#Stereo MP3
			with Ticker("  Creating Stereo MP3 file..."):
				makemp3(item)
		elif no_channels == 1:
			with Ticker("  Inserting the data to MySQL..."):
				tomysql(item, deploymentID, item, samprate, no_channels)
			print " "
			with Ticker("  Drawing waveform and spectrogram..."):
				draw_png(item)
			print " "
			with Ticker("  Creating Stereo MP3 file..."):
				makemp3(item)
		print " "
		itemflac=item[:-4] + ".flac"
		with Ticker("  Cleaning up..."):
			cleanup(working_dir,pngmp3_dir,deploymentID,itemflac)

print " "
#Creating a done file to indicate it was processed
fileHandle = open ( working_dir + '/done.txt', 'w' )
process_date = datetime.datetime.now().strftime("\n   Processed on %d/%m/%Y at %I:%M %p\n")
fileHandle.write ( process_date )
fileHandle.close() 


print "\n  Folder DONE!"
