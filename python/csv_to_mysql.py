#!/usr/bin/python
# v. 14 aug 2013
"""
Script to copy data from csv files to a MySQL table.
"""

#########################################################################
# SETTINGS								#
#########################################################################

db_hostname=''
db_database=''
db_username=''
db_password=''
directory_to_check=''

#########################################################################
# HEADER DECLARATIONS							#
#########################################################################

import commands
import os
import sys
import shutil

try:
	import MySQLdb
except:
	print "\n MySQLdb is not installed. To install in Ubuntu use: \n   sudo apt-get install python-mysqldb\n"
	sys.exit (1)


#########################################################################
# FUNCTION DECLARATIONS							#
#########################################################################

def insert(SoundID, adi_left, shannon_left, db_value):
	#Open MySQL
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit (1)
	cursor = con.cursor()
	query = "REPLACE INTO Indices (SoundID, adi_left, shannon_left, db_value) \
         VALUES (" + \
	`SoundID` + ', ' + `adi_left` + ', ' + `shannon_left` + ', ' + `db_value` + ')'
	#print "Query: " + query + "\n"
	cursor.execute(query)
	con.commit()
	SoundID=con.insert_id()
	#Close MySQL
	cursor.close()
	con.close()
	return


#########################################################################
# EXECUTE THE SCRIPT							#
#########################################################################


csv_files = os.listdir(directory_to_check)
os.chdir(directory_to_check)

for this_file in csv_files:
	if this_file[-3:] == "csv":
		#f = open("this_file", 'r')

		with open(this_file) as f:
			content = f.readlines()
		for this_line in content:
			this_line = this_line.replace('\r\n','')
			
			insert(str(this_file.split('.')[0]), str(this_line.split(',')[0]), str(this_line.split(',')[1]), str(this_line.split(',')[2]))
		print " Done with file " + this_file + "\n\n"

