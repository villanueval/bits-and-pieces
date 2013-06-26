#/bin/bash
#
#Script to weekly get a copy of a website and store an incremental copy

thisdir="/home/user/wget"

#under this dir, there are two: "archive", where each version is stored,
# and "running", where the script is hosted and ran from. There should be
# a file called sites.txt under "running" with two variables per line:
# URL SiteName

cd $thisdir/running

date=`date "+%Y%m%d"`

cat sites.txt | while read site name
do
	wget -mk -np $site

	for file in *; do
		if [ -d $file ]; then
		mv $file $name$date
	      
		if [ -d "$thisdir/archive/$name" ];then
			rsync -ah --progress --link-dest="$thisdir/archive/$name/" \
			$name$date \
			$thisdir/archive/$name$date

			rm -r $name$date
		else
			mv $name$date $thisdir/archive/$name
		fi
	   fi
	done
done

