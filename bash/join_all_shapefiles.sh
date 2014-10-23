#!/bin/bash
#
# This script will merge all shapfiles in the directory to a new one called merge.shp
#
for f in *.shp; do 
	ogr2ogr -update -append merge.shp $f -nln merge
done