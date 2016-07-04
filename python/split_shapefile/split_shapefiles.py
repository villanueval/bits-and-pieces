#!/usr/bin/python
#

# Import modules
import commands, shutil, os, sys, time
from osgeo import ogr
# from osgeo import osr
# from glob import glob


# Test command line variables
if len(sys.argv) != 4:
  print "\n Error: Incorrect number of arguments given."
  print " Call the program as: " + sys.argv[0] + " <shp_file without the .shp extension> <field> <startid>"
  print " "
  print " Exiting program."
  print " "
  sys.exit(1)

#get cli arguments
this_file = sys.argv[1]
field =  sys.argv[2]
startid =  int(sys.argv[3])


#Create or append to species file with the data in csv
exportfile = open ("species.csv", "a")


#make dir to hold the shapefiles
if not os.path.exists(this_file):
    os.makedirs(this_file)

#from http://gis.stackexchange.com/a/115065
ogr_ds = ogr.Open(this_file + '.shp')
sql = 'SELECT DISTINCT ' + field + ' FROM ' + this_file
layer = ogr_ds.ExecuteSQL(sql)
featureCount = layer.GetFeatureCount()
print "\n There are " + str(featureCount) + " features in this dataset \n"
time.sleep(2)
for i, feature in enumerate(layer):
	print('%d: %s' % (i + startid, feature.GetField(0)))
	exportfile.write('%s,%d,%s\n' % (this_file, i + startid, feature.GetField(0)))
	#ogr2ogr, to save time in writing
	status, output = commands.getstatusoutput('ogr2ogr -dialect SQLITE -sql "SELECT * FROM ' + this_file + ' WHERE ' + field + '=\'' + feature.GetField(0) + '\'" ' + this_file + '/' + str(i + startid) + '.shp ' + this_file + '.shp')
	

#close file
exportfile.close()
