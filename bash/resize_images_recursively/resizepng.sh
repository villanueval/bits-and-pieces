#!/bin/bash
#
#
for i in *.png; do
	convert $i   -resize 600x300\!  ${i%.png}.1.png
	rm $i
	mv ${i%.png}.1.png $i
done
