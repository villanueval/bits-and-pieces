#!/usr/bin/python

# Import modules
import commands
import os

#Functions

def extractflac(item):
  #Extract the wav from the flac, forcing overwrite
	 status, output = commands.getstatusoutput('flac -df ' + item)
	#Get filename with the .wav extention
	 item_wav=item[:-5] + ".wav"
	if status != 0:
	    print "Problem with file ", item[:-5]
	    print " The file is corrupted or not a flac file!!!"
	else:
	    print "done!"
	return item_wav


#Execute

ls = os.listdir(os.curdir)
for item in ls:
	if item[-5:] == ".FLAC" or item[-5:] == ".flac":
		print "Extracting: ", item
		extractflac(item)
