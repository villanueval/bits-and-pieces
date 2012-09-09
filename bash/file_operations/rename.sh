#!/bin/bash
#
for i in *.flac
	do
	#replace "Disc 2 - " with nothing
	# To replace it with "disc2":
	#j=`echo $i | sed 's/Disc 2 - /disc2/g'`
	j=`echo $i | sed 's/Disc 2 - //g'`
	mv "$i" "$j"
	done

exit 0
