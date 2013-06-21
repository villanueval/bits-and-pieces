#/bin/bash

#first, test that encfs is installed
#from http://stackoverflow.com/a/6471205
hash encfs &> /dev/null
if [ $? -eq 1 ]; then
	echo ""
	echo " Error: encfs is not installed, leaving script"
	echo ""
	exit
fi

#What to backup, ususally your home folder, i.e. /home/user
DIR_TOBACKUP="/home/user"
#Where to mount, i.e. "private"
DIRECTORY=""
#Where encfs will store the files, i.e. ".private"
ENCFS_DIR=""

encfs ENCFS_DIR $DIRECTORY

if [ $? -eq 1 ]; then
	echo ""
	echo " Error: encfs could not mount the encypted folder, leaving script"
	echo ""
	exit
fi

#alt way when looking for a particular folder inside the encrypted folder
#if [ -d "/dir" ]; then

	date=`date "+%Y-%m-%d_%H%M%S"`

	echo ""
	echo "   Backup working"
	echo ""

	#MYSQL
		#echo ""
		#echo "   Backing up MySQL databases..."
		#echo ""
		
		#Option1
			#This uses a user called "backupuser" with a password "Password"
			# Be mindful of security, as an alternative, see the version below
			#mysqldump -u backupuser -pPassword database > $DIRECTORY/MySQL/database.sql

		#Option2
			#Ask for MySQL password
			#echo ""
			#echo "Enter MySQL root password:"
			#echo ""

			#stty -echo
			#read mysqlpassword
			#stty echo
			#mysqldump -u backupuser -p$mysqlpassword database > $DIRECTORY/MySQL/database.sql
	
		#compress using tar
		#cd $DIRECTORY/MySQL/
		#tar -cvzf mysql-$date.tar.gz *.sql
		#rm *.sql

		#cd

	echo ""
	echo "   Backing up Documents and files..."
	echo ""

	mkdir $DIRECTORY/$date

	rsync -ah --progress --delete --link-dest=$DIRECTORY/current/ \
		$DIR_TOBACKUP \
		$DIRECTORY/$date/

	#New current link and cleanup
	rm -f $DIRECTORY/current

	cd $DIRECTORY/
	ln -s $date current

	cd

	fusermount -u $DIRECTORY

	echo ""
	echo "   Backup done!"
	echo ""

fi
