#/bin/bash
# 10 Jul 2012


date=`date +%Y-%m-%d_%H%M%S`
thismachine=$(hostname)
thisuser=`whoami`

echo ""
echo "   Backing up MySQL databases..."
echo ""

mkdir /home/$thisuser/backup/current
cd /home/$thisuser/backup/current

mysqldump -q -u backupuser -p<password> wiki > wiki.sql

tar -cvzf $thismachine-mysql-$date.tar.gz *.sql

tarexit=$(echo $?)
	if [ "$tarexit" -ne 0 ]
	then
		echo "Mysql backup fail!";
	fi

rm *.sql


echo ""
echo "   MySQL Backup complete."
echo ""

echo ""
echo "   Backing up www..."
echo ""

cd /

tar -cvzf /home/$thisuser/backup/current/$thismachine-www-$date.tar.gz /var/www/

tarexit=$(echo $?)
	if [ "$tarexit" -ne 0 ]
	then
		echo "Tar of www failed!";
	fi

echo ""
echo "   WWW Backup complete."
echo ""

echo ""
echo "   Copying to Humboldt..."
echo ""

echo "put $thismachine-mysql-$date.tar.gz : /home/lvillanu/backups/$thismachine-mysql-$date.tar.gz" > /home/$thisuser/backup/current/files
echo "put $thismachine-www-$date.tar.gz : /home/lvillanu/backups/$thismachine-www-$date.tar.gz" >> /home/$thisuser/backup/current/files

cd /home/$thisuser/backup/current

##########################################################################
##CHANGE USERNAME BELOW TO ALLOW UPLOAD TO FORTRESS WITH ANOTHER ACCOUNT #
##########################################################################
/opt/hsi/bin/hsi -l lvillanu < files

tarexit=$(echo $?)
	if [ "$tarexit" -ne 0 ]
	then
		echo "Copy to Humboldt fail!";
	fi

cd /home/$thisuser/backup/

rm -r current

