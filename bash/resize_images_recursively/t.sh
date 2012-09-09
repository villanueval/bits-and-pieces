#!/bin/bash
#
for dir in `ls -d */`
do
	cp resizepng.sh $dir
	cd $dir
	./resizepng.sh
	rm resizepng.sh
	cd ..
done
