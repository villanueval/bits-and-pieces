#/bin/bash

while :
do

	./check_auxfiles.py

	echo ""
	echo "All done. Waiting an hour..."
	echo ""

	sleep 3600

done
