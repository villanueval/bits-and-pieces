#!/bin/bash
#
#Bash script that goes to every directory in the current path and does a git commit, push, and then pull.
# Useful when your git clones are all in the same directory and work from different workstations.
#
for gitarchive in *; do
   if [ -d $gitarchive ]; then
      cd $gitarchive
      git pull
      git add -A
      git commit -a
      git push origin master
      cd ..
   fi
done
