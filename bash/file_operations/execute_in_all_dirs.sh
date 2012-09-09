#!/bin/bash
#
for file in *; do
   if [ -d $file ]; then
      cp run.sh $file/
      cp script.R $file/
      cd $file
      ./run.sh
      cd ..
   fi
done
