#!/usr/bin/python

"""
Get a siteID from the database using the ColID
"""

#########################################################################
# HEADER DECLARATIONS							#
#########################################################################

# Import modules
import commands
import os
import sys

try:
	import MySQLdb
except:
	print "\n MySQLdb is not installed. To install in Ubuntu use: \n   sudo apt-get install python-mysqldb\n"
	sys.exit (1)


# Test "global" variables
if len(sys.argv) < 2:
	print "\n Incorrect number of arguments given."
	print "\n Call the program as: " + sys.argv[0] + " <ColID>"
	print "\n Exiting program.\n"
	sys.exit(1)

ColID = str(sys.argv[1])

db_hostname=''
db_database=''
db_username=''
db_password=''


def getsite(siteid):
        try:
                con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database)
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
        cursor = con.cursor()
        query = "SELECT SiteID FROM Deployment WHERE DeploymentID='" + ColID + "' LIMIT 1";
        cursor.execute (query)
        if cursor.rowcount==0:
                print str(0)
                sys.exit(0)
        row = cursor.fetchone ()
        cursor.close ()
        con.close ()
        return row[0]

SiteID1=getsite(ColID)

SiteID=int(SiteID1) + 101

print str(SiteID)
