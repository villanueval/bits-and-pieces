#!/bin/bash
#
# wav2mp3
#
for i in *.wav; do
	# 192 is the bitrate
	lame -h -b 192 $i ${i%.wav}.mp3
done
