#!/usr/bin/python
#
# Get attribute list from a shapefile

# Import modules
import commands, shutil, os, sys
from osgeo import ogr
# from osgeo import osr
# from glob import glob


# Test command line variables
if len(sys.argv) != 4:
  print "\n Error: Incorrect number of arguments given."
  print " Call the program as: " + sys.argv[0] + " <shp_file without the .shp extension> <field/attribute> <startid>"
  print " "
  print " Exiting program."
  print " "
  sys.exit(1)

#get cli arguments
this_file = sys.argv[1]
field =  sys.argv[2]


#Create or append to results file
exportfile = open (field + ".csv", "a")


#from http://gis.stackexchange.com/a/115065
ogr_ds = ogr.Open(this_file + '.shp')
sql = 'SELECT DISTINCT ' + field + ' FROM ' + this_file
layer = ogr_ds.ExecuteSQL(sql)
for i, feature in enumerate(layer):
	print('%s' % (feature.GetField(0)))
	exportfile.write('%s\n' % (feature.GetField(0)))
	

#close file
exportfile.close()
