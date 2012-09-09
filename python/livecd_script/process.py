#!/usr/bin/python
# v. 18 apr 09
"""
Main script to trigger R or Python scripts stored in a MySQL database.
This script is to be used in LiveCDs and ran from Windows machines during the night/weekend.
"""

#########################################################################
# HEADER DECLARATIONS							#
#########################################################################
 
# Import modules
import commands
import os
import sys
import MySQLdb
import datetime
import time

#########################################################################
# GLOBAL VARIABLES							#
#########################################################################

#Save computer name
# since its a LiveCD for each computer, hostname may not be accurate.
if os.path.exists('compname.txt'):
	f = open ( 'compname.txt', 'r' )
	computer_name=f.read()
	f.close()
	computer_name = computer_name[:-1]
else:
	computer_name = 'unknown'

db_hostname = ''
db_user = ''
db_password = ''
db_database = ''


#########################################################################
# FUNCTION DECLARATIONS							#
#########################################################################
 

#Extract wav from FLAC
def extractflac(fileID,item,filename,computer_name="unknown",get_method="share"):
	item_wav = filename[:-4] + 'wav'
	if get_method=="share":
		status, output = commands.getstatusoutput('cp ' + item + ' .')
		if status != 0:
			print output
			logdb(fileID, computer_name, "Problem with FLAC file: " + item + ". " + output)
			updatefile(fileID, 3)
			return 1
		else:
			status, output = commands.getstatusoutput('flac -dFfs ' + filename + ' -o ' + item_wav)
			logdb(fileID, computer_name, "FLAC file extract was successful: " + item + ". " + output)
			os.remove(filename)
			return item_wav
	elif get_method=="web":
		status, output = commands.getstatusoutput('wget ' + item)
		if status != 0:
			print output
			logdb(fileID, computer_name, "Problem with FLAC file: " + item + ". " + output)
			updatefile(fileID, 3)
			return 1
		else:
			status, output = commands.getstatusoutput('flac -dFfs ' + filename + ' -o ' + item_wav)
			logdb(fileID, computer_name, "FLAC file extract was successful: " + item + ". " + output)
			os.remove(filename)
			return item_wav


#Get the script from MySQL
def getscript(scriptID):
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_user, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "\n\n Database Error %d: %s" % (e.args[0], e.args[1])
		print "\n Could not connect to the database! leaving the program..."
		sys.exit (1)
	cursor = con.cursor()
	query = "SELECT Language, Script FROM Scripts WHERE ScriptID='" + str(scriptID) + "' LIMIT 1";
	cursor.execute (query)
	row = cursor.fetchone ()
	cursor.close ()
	con.close ()
	return row




#Get the number of tasks completed by this computer
def get_no_tasks(computer_name):
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_user, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "\n\n Database Error %d: %s" % (e.args[0], e.args[1])
		print "\n Could not connect to the database! leaving the program..."
		sys.exit (1)
	cursor = con.cursor()
	query = "SELECT COUNT(*) AS Done FROM FileQueue WHERE ProcessDoneComputer='" + computer_name + "' AND Status='2'";
	cursor.execute (query)
	row = cursor.fetchone ()
	cursor.close ()
	con.close ()
	return row


#Get a file to process from MySQL
def getfile():
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_user, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "Database Error %d: %s" % (e.args[0], e.args[1])
		print "\n Could not connect to the database! leaving the program..."
		sys.exit (1)
	cursor = con.cursor()
	query = "SELECT FileQueueID, FileID, Method, Server, Path, Filename, ScriptID FROM FileQueue WHERE Status='0' ORDER BY Priority, FileQueueID LIMIT 1";
	cursor.execute (query)
	row = cursor.fetchone ()
	cursor.close ()
	con.close ()
	return row


#Update status in MySQL
def updatefile(fileID, statusID, computer_name="unknown"):
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_user, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "Database Error %d: %s" % (e.args[0], e.args[1])
		print "\n Could not connect to the database! leaving the program..."
		sys.exit (1)
	cursor = con.cursor()
	if statusID==0:
		query = "UPDATE FileQueue SET Status='" + str(statusID) + "' WHERE FileQueueID='" + str(fileID) + "'"
	elif statusID==1:
		query = "UPDATE FileQueue SET Status='" + str(statusID) + "', ClaimedDate=NOW() WHERE FileQueueID='" + str(fileID) + "'"
	elif statusID==2:
		query = "UPDATE FileQueue SET Status='" + str(statusID) + "', ProcessDoneDate=NOW(), ProcessDoneComputer='" + computer_name + "' WHERE FileQueueID='" + str(fileID) + "'"
	elif statusID==3:
		query = "UPDATE FileQueue SET Status='" + str(statusID) + "' WHERE FileQueueID='" + str(fileID) + "'"
	cursor.execute (query)
	return


#Write log to MySQL
def logdb(fileID, computer_name, log):
	log = log.replace('"', '\"').replace("'", "\'")
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_user, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "Database Error %d: %s" % (e.args[0], e.args[1])
		print "\n Could not connect to the database! leaving the program..."
		sys.exit (1)
	cursor = con.cursor()
	query = "INSERT INTO FilesLog (`FileQueueID` ,`Computer` ,`TimeStamp` ,`FileLog`) VALUES ('" + str(fileID) + "', '" + computer_name + "', NOW() , %s)"
	cursor.execute (query, (log,))
	return

 
#########################################################################
# EXECUTE THE SCRIPT							#
#########################################################################


#Clean up directory, just in case
status, output = commands.getstatusoutput('rm *.wav')
status, output = commands.getstatusoutput('rm *.flac')
status, output = commands.getstatusoutput('rm script.*')

status=''
output=''

while True:

	no_tasks = get_no_tasks(computer_name)
	no_tasks = int(no_tasks[0])
	print " ====================================================="
	print " This computer has completed " + str(no_tasks) + " tasks."
	print " ====================================================="
	#The following is to mantain a way to allow the user to cancel the program
	# while exiting in a clean manner
	# from http://effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
	try:

		#Get the file and the path from MySQL
		print " Getting a file to process from the server...\n"
		row = getfile()
		if row==None:
			print " No new files are waiting in the queue...\n  waiting for a minute..."
			print " To stop, press Ctrl-c\n"
			time.sleep(60) #Sleep for 1 minute, then try again.

		elif len(row)==7:
			fileID, orig_fileID, get_method, server, filepath, filename, scriptID = row
			fileID = int(fileID)
			orig_fileID = int(orig_fileID)
			scriptID = int(scriptID)

			if get_method=="share":
				file_to_process='/mnt/' + server + filepath + '/' + filename
				print " Processing file " + file_to_process
			elif get_method=="web":
				file_to_process='http://' + server + filepath + '/' + filename
				print " Processing file " + file_to_process

			#update the record on MySQL as taken
			updatefile(fileID, 1)

			#extract wav from flac file
			print " Extracting file from server...\n"
			wav_file=extractflac(fileID,file_to_process,filename,computer_name,get_method)

			#Check that the wav file was extracted from the flac
			if wav_file==1:
				print "There was a problem with file " + file_to_process
				print " Cleaning up...\n "
				updatefile(fileID, 3)
				logdb(fileID, computer_name, "Problem with file: " + output)
				del(fileID)
			else:
				#get the script
				language, script = getscript(scriptID)

				if language=="R":
					print " Executing R script...\n\n"
					print " To stop, press Ctrl-c\n"
					#save the script obtained from the database in a file
					scriptfile = open ( 'script.R', 'w' )
					scriptfile.write (script)
					scriptfile.close()
					#execute R script on file
					status, output = commands.getstatusoutput('Rscript --vanilla script.R ' + wav_file + ' ' + str(orig_fileID))
					print status
					print output
					if status != 0:
						print "There was a problem with file " + file_to_process
						print " or with the script " + scriptID
						print " "
						print output
						print " Cleaning up...\n "
						commands.getstatusoutput('rm *.wav')
						os.remove('script.R')
						updatefile(fileID, 3)
						logdb(fileID, computer_name, "Problem with file or script: " + output)
						del(fileID)
					else:
						logdb(fileID, computer_name, datetime.datetime.now().strftime("Script completed on %d/%b/%y %H:%M\n") + output)
						commands.getstatusoutput('rm *.wav')
						os.remove('script.R')
						updatefile(fileID, 2, computer_name)
						del(fileID)
						print "  Script completed.\n"


				elif language=="Python":
					print "\n\n Executing Python script..."
					print "\n\n To stop, press Ctrl-c"
					#save the script obtained from the database in a file
					scriptfile = open ( 'script.py', 'w' )
					scriptfile.write (script)
					scriptfile.close()
					#execute R script on file
					status, output = commands.getstatusoutput('python script.py ' + wav_file + ' ' + str(orig_fileID))
					if status != 0:
						print "There was a problem with file " + file_to_process
						print " or with the script " + scriptID
						print " "
						print output
						print "\n  Cleaning up..."
						commands.getstatusoutput('rm *.wav')
						os.remove('script.py')
						updatefile(fileID, 3)
						logdb(fileID, computer_name, "Problem with file or script: " + output)
						del(fileID) 
					else:
						logdb(fileID, computer_name, datetime.datetime.now().strftime("Script completed on %d/%b/%y %H:%M\n") + output)
						commands.getstatusoutput('rm *.wav')
						os.remove('script.py')
						updatefile(fileID, 2, computer_name)
						del(fileID)
						print "  Script completed.\n"



	except (KeyboardInterrupt):
		print "\n\n Interrupt command received...\n  cleaning up, please wait..."

		#Clean up directory
		commands.getstatusoutput('rm *.wav')
		commands.getstatusoutput('rm *.flac')
		commands.getstatusoutput('rm script.*')

		#If fileID exists, use it to update the database, otherwise use 0
		try:
			fileID
		except NameError:
			logdb(0, computer_name, datetime.datetime.now().strftime("Script keyboard-interrupted on %d/%b/%y %H:%M\n") + output)
		else:
			updatefile(fileID, 0)
			logdb(fileID, computer_name, datetime.datetime.now().strftime("Script keyboard-interrupted on %d/%b/%y %H:%M\n") + output)
		print " To restart analysis, type:  earrestart\n and press [ENTER]\n"
		print " To shutdown, type:  earshutdown\n and press [ENTER]\n"
		sys.exit (0) #Exit normally
	except (SystemExit):
		print "\n\n Ending program...\n  cleaning up, please wait..."
		#If fileID exists, use it to update the database, otherwise use 0
		try:
			fileID
		except NameError:
			logdb(0, computer_name, datetime.datetime.now().strftime("Script ended on %d/%b/%y %H:%M\n") + output)
		else:
			logdb(fileID, computer_name, datetime.datetime.now().strftime("Script ended on %d/%b/%y %H:%M\n") + output)
			updatefile(fileID, 0)

		print " To restart analysis, type:  earrestart\n and press [ENTER]\n"
		print " To shutdown, type:  earshutdown\n and press [ENTER]\n\n"
		sys.exit (0) #Exit normally
	except:
		print "\n\n Unknown error, cleaning up, please wait..."
		print status
		print output
		#If fileID exists, use it to update the database, otherwise use 0
		try:
			fileID
		except NameError:
			logdb(0, computer_name, datetime.datetime.now().strftime("Script ended unexpectedly on %d/%b/%y %H:%M\n") + output)
		else:
			logdb(fileID, computer_name, datetime.datetime.now().strftime("Script ended unexpectedly on %d/%b/%y %H:%M\n") + output)
			updatefile(fileID, 3)

		#Clean up directory
		commands.getstatusoutput('rm *.wav')
		commands.getstatusoutput('rm *.flac')
		commands.getstatusoutput('rm script.*')


