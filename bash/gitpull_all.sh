#!/bin/bash
#
#Bash script that goes to every directory in the current path and does a git pull.
# Usefull when your git clones are all in the same directory.
#
for gitarchive in *; do
   if [ -d $gitarchive ]; then
      cd $gitarchive
      git pull
      cd ..
   fi
done
