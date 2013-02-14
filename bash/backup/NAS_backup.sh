#/bin/bash
#
# Backup particular folders in our NAS that have been
#  specified in a file

file="dirs_to_backup.txt"
#local dir where the nas is mounted, with trailing slash
# for example: /mnt/nas/
root_dir="/mnt/nas/"

cd $root_dir
fromdos $file
#save each line to the array
array=($(<$file))

#iterate over the array
for i in "${array[@]}"
	do
	this_dir=$root_dir$i
	cd $this_dir
	#Add command for backup and moving files here
	pwd
done

cd $root_dir
todos $file

