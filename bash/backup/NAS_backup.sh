#/bin/bash
#
#Backup particular folders in our NAS that have been
# specified in a file with two fields, separated by a comma,
# per line:
#  
#   archive_name,path
#
#Where archive_name is the name for the tar file
#

file="dirs_to_backup.txt"
#local dir where the nas is mounted, with trailing slash
# for example: /mnt/nas/
root_dir="/mnt/nas/"

cd $root_dir

#Prepare files when dealing with Windows users
fromdos $file

#change Windows slashes | from http://ubuntuforums.org/showpost.php?p=4684331&postcount=10
echo dirs_to_backup.txt | while read file
do 
	awk '{ gsub( /\\/, "/" ); print }' $file > $file.$$
	mv $file.$$ $file
done

#save each line to the array
array1=($(<$file))

#iterate over the array
for i in "${array1[@]}"
	do
	#Ignore files that start with pound (#)
	if [[ ${i:0:1} == '#' ]]
	then
		echo ""
	else
		#from http://stackoverflow.com/a/10586169
		IFS=',' read -a array2 <<< "$i"
	
		fullpath="${array2[1]}"
		tarname="${array2[0]}"
		
		#Add command for backup and moving files here
		tar -cvf $tarname.$date.tar $fullpath
	fi
done

todos $file

