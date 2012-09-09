#/bin/bash

tempdir=/home/ljvillanueva/tip2012/flac

#while :
#do
	#First script
	cd $tempdir
	for ColID in *
	do
		if [ -d "$ColID" ]
		then
			SiteID=$(/home/ljvillanueva/tip2012/scripts/getsite.py $ColID)
			if [ "$SiteID" -eq 0 ]
			then
				break
			fi

			#cd $tempdir/READY
			#mv $ColID ../WORKING/$ColID
			cd $ColID
			echo ""
			echo "Compressing files to flac..."
			echo ""
			flac -V --delete-input-file *.wav

			#Make tar
			echo ""
			echo "Compressing to tar..."
			echo ""
			
			cd /home/ljvillanueva/tip2012/tars
			/home/ljvillanueva/tip2012/scripts/tarfiles.py $tempdir $ColID
			tarexit=$(echo $?)
			if [ "$tarexit" -ne 0 ]
			then
				/home/ljvillanueva/tip2012/scripts/tarfiles.py $tempdir $ColID
				tarexit=$(echo $?)
				if [ "$tarexit" -ne 0 ]
				then
					echo "Tar fail!";
					exit 0;
				fi
			fi
			
			#Add commands to upload with hsi
			#then, just use >> hsi -l lvillanu < /home/ljvillanueva/tip2012/tars/files
			echo "put $ColID.tar" >> /home/ljvillanueva/tip2012/tars/files 
			
			#Check and insert to db
			echo ""
			echo "Adding files to database..."
			echo ""
			cd $tempdir
			/home/ljvillanueva/tip2012/scripts/addfiles.py $tempdir/$ColID $ColID $SiteID
		
			mv $tempdir/$ColID /home/ljvillanueva/tip2012/done/
			echo ""
			echo "Done..."
			echo ""
		fi
	done

#	echo ""
#	echo "Checking aux files..."
#	echo ""
#	cd $curdir
#	./check_auxfiles.py

#	echo ""
#	echo "All done. Waiting an hour..."
#	echo ""
	#ALL DONE, WAIT FOR TOMORROW AT MIDNIGHT
	# adapted from http://stackoverflow.com/questions/645992/bash-sleep-until-a-specific-time-date
	#current_epoch=$(date +%s)
	#target_epoch=$(date -d 'tomorrow 00:00' +%s)
	#sleep_seconds=$(( $target_epoch - $current_epoch ))
	#sleep $sleep_seconds
#	sleep 3600

#done
