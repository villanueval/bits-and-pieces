#/bin/bash

tempdir=/soundfiles/$1
touch /soundfiles/tars/files

#while :
#do
	#First script
	cd $tempdir
	for dirtotar in *
	do
		if [ -d "$dirtotar" ]
		then
			#Make tar
			echo ""
			echo "Compressing to tar..."
			echo ""
			
			/soundfiles/tarfiles.py $tempdir $dirtotar
			tarexit=$(echo $?)
			if [ "$tarexit" -ne 0 ]
			then
				/soundfiles/tarfiles.py $tempdir $dirtotar
				tarexit=$(echo $?)
				if [ "$tarexit" -ne 0 ]
				then
					echo "Tar fail!";
					exit 1;
				fi
			fi
			
			mv $dirtotar.tar /soundfiles/tars/
			
			#Add commands to upload with hsi
			#then, just use >> hsi -l lvillanu < /home/ljvillanueva/tip2012/tars/files
			echo "put $dirtotar.tar : /home/lvillanu/hoosier_electric/$dirtotar.tar" >> /soundfiles/tars/files 
			
		fi
	done



##########################################################################
##CHANGE USERNAME BELOW TO ALLOW UPLOAD TO FORTRESS WITH ANOTHER ACCOUNT #
##########################################################################
/opt/hsi/bin/hsi -l lvillanu < files

tarexit=$(echo $?)
	if [ "$tarexit" -ne 0 ]
	then
		echo "Copy to Humboldt fail!";
	fi


