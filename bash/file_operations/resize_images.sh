#!/bin/bash
#
#using imagemagick
for i in *.png
	do

	convert $i -resize 1000x1000 ${i%.png}1.png
	rm $i
	done

exit 0
