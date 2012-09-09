#/bin/bash

date=`date "+%Y-%m-%d_%H%M%S"`

echo ""
echo "   Backup working"
echo ""


echo ""
echo "Enter MySQL root password:"
echo ""

stty -echo
read password
stty echo

echo ""
echo "   Backing up MySQL databases..."
echo ""

mysqldump -u root -p$password wiki > /media/truecrypt1/MySQL/wiki.sql

cd /media/truecrypt1/MySQL

tar -cvzf mysql-$date.tar.gz *.sql

rm *.sql

echo ""
echo "   Backing up Documents and files..."
echo ""

mkdir /media/truecrypt1/$date
mkdir /media/truecrypt1/$date/Linux
mkdir /media/truecrypt1/$date/Linux/home/
mkdir /media/truecrypt1/$date/Linux/www/
mkdir /media/truecrypt1/$date/Linux/vm/
mkdir /media/truecrypt1/$date/Windows/
mkdir /media/truecrypt1/$date/iTunes/

rsync -aP --delete --link-dest=/media/truecrypt1/current/Linux/home/ \
	/home/ljvillanueva/ \
	/media/truecrypt1/$date/Linux/home/

echo ""
echo "   Backing up VM..."
echo ""

rsync -aP --delete --link-dest=/media/truecrypt1/current/Linux/vm/ \
	/vm/ \
	/media/truecrypt1/$date/Linux/vm/


echo ""
echo "   Backing up www..."
echo ""

rsync -aP --delete --link-dest=/media/truecrypt1/current/Linux/www/ \
	/var/www/ \
	/media/truecrypt1/$date/Linux/www/



echo ""
echo "   Backing up Windows 7 folders..."
echo ""

rsync -rthP --delete --link-dest=/media/truecrypt1/current/Windows/ \
	/windows/Users/ljvillanueva/Documents \
	/windows/Users/ljvillanueva/Desktop \
	/windows/Users/ljvillanueva/AppData \
	/media/truecrypt1/$date/Windows/

rsync -rthP --delete --link-dest=/media/truecrypt1/current/Windows/ \
	/windows/Users/ljvillanueva/Music \
	/media/truecrypt1/$date/iTunes/

#New current link and cleanup
rm -f /media/truecrypt1/current

cd /media/truecrypt1/
ln -s $date current

echo ""
echo "   Backup done!"
echo ""

