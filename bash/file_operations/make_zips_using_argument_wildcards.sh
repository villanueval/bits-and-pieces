#!/bin/bash
#
#Escape wildcards
# example: ./script.sh 12\?
dir="$1"
maindir="/mnt/humboldt/users/lvillanu/WinHPC/laselvadata"
todir="/mnt/humboldt/users/lvillanu/WinHPC/zips/"

for file in $maindir/$dir; do
   if [ -d $file ]; then     
      #compress csv indices
      mv $file.*.csv . 
      zip $file.zip $file.*.csv
      rm $file.*.csv

      #compress polygons
      mv $file .
      zip -r $file.polygons.zip $file
      rm -r $file
      #move everything
      
      mv *.zip $todir

   fi
done
