#!/bin/bash
#
#rename some part of the filename
#
# run like: ./rename_partial.sh old_name new_name

for file in *
	do
		mv $file ${file//$1/$2}
	done

exit 0
