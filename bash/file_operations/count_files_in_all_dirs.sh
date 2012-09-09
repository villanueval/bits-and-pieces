#!/bin/bash
#
for dirs in *; do
   if [ -d $dirs ]; then
      this_count=`ls -1 $dirs | wc -l`
      echo $dirs $this_count
   fi
done
