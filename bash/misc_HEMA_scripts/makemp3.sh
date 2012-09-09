#/bin/sh
#

		for i in *.flac; do
			flac -fd $i -o temp.wav
			sox temp.wav temp1.wav rate 22050
			lame --noreplaygain -f -b 128 temp1.wav ${i%.wav}.autopreview.mp3
			rm *.wav
		done
exit 0
