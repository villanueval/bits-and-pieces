#/bin/sh
#

		for i in *.mp3; do
			mv $i ${i%.flac.autopreview.mp3}.autopreview.mp3
		done
exit 0
