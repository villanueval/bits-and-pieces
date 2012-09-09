#!/usr/bin/python

"""
Script with functions to query one/multiple rows and to insert to a MySQL database.
14 jun 08
"""

#################################################################################################
# HEADER DECLARATIONS										#
#################################################################################################

# Import modules
import MySQLdb
import sys
import wave

# Test "global" variables
if len(sys.argv) != 6:
	print "\nIncorrect number of arguments given.\n"
	print "Call the program as: " + sys.argv[0] + " <wav file> <deployment_ID> <filename> <samp_rate> <no_channels>\n"
	print "Exiting program.\n"
	sys.exit()

# Place "global" variables in the namespace
wave_item = sys.argv[3]
deployment_ID = sys.argv[2]
file_name = sys.argv[3]
samp_rate = sys.argv[4]
nochannels = sys.argv[5]

#################################################################################################
# FUNCTION DECLARATIONS										#
#################################################################################################

def insert(deployment_ID, filename, soundformat, no_channels, samplingrate, bitres, soundlength, sounddate, soundtime):
	#Open MySQL
	try:
		con = MySQLdb.connect(host='', user='', passwd='', db='')
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit (1)
	cursor = con.cursor()
	query = "INSERT INTO Sample (DeploymentID, SampName, SampFormat, SampChannels, SampRate, SampBitRes, SampLength, SampDate, SampTime) \
         VALUES (" + \
	`deployment_ID` + ', ' + `filename` + ', ' + `soundformat` + ', ' + `no_channels` + ', ' + `samplingrate` + ', ' + `bitres` + ', ' + `soundlength` + ', ' + `sounddate` + ', ' + `soundtime` + ")"
	#print "Query: " + query + "\n"
	cursor.execute (query)
	print "ID of row inserted: %s" % con.insert_id()
	#Close MySQL
	cursor.close ()
	con.close ()
	return

def open_wave(wave_file):
	"""
	Open the wave file specified in the command line or elsewhere for processing.
	"""
	wave_pointer = wave.open(wave_file,'rb')
	return wave_pointer

def find_values(wave_pointer):
	"""
	Read the values to fill the "wave_vars" array from the sound file.
	"""
	wave_vars = {}
	wave_vars['samp_rate'] = wave_pointer.getframerate()
	wave_vars['num_samps'] = wave_pointer.getnframes()
	wave_vars['samp_width'] = wave_pointer.getsampwidth()
	wave_vars['no_channels'] = wave_pointer.getnchannels()
	if wave_vars['samp_width'] == 1:
		# The data are 8 bit unsigned
		wave_vars['bit_code'] = 'B'
		wave_vars['bits'] = '8'
	elif wave_vars['samp_width'] == 2:
		# The data are 16 bit signed
		wave_vars['bit_code'] = 'h'
		wave_vars['bits'] = '16'
	elif wave_vars['samp_width'] == 4:
		# The data are 32 bit signed
		wave_vars['bit_code'] = 'i'
		wave_vars['bits'] = '32'
	else:
		# I don't know what the hell it is
		print "I don't know what the hell bit width you're using."
		sys.exit()
	wave_vars['max_time'] = wave_vars['num_samps'] / wave_vars['samp_rate']
	# Print wave file values, mostly to debug
	#print "Wave values: "
	#for item in wave_vars.iteritems():
	#	print item
	return wave_vars

#################################################################################################
# CODE EXECUTION										#
# They say that calling functions this way is bad form, but it works for my purposes. Why would #
# anyone want to go to all the trouble of writing a complicated module, when they can just run	#
# some simple commands?										#
#################################################################################################

SampDate = wave_item[5:9] + "-" + wave_item[9:11] + "-" + wave_item[11:13]

SampTime = wave_item[14:16] + ":00"

NameInsert = file_name[:-4] + ".flac"

wave_pointer = open_wave(wave_item)

wave_vars = find_values(wave_pointer)

insert(deployment_ID, NameInsert, 'FLAC', nochannels, samp_rate, wave_vars['bits'], wave_vars['max_time'], SampDate, SampTime)

