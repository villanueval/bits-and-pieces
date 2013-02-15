#!/bin/sh
#
#Removes empty lines in text files.

files="/a_dir_with_txt_files/*.txt"
for i in $files
do
  sed '/^$/d' $i > $i.out
  mv  $i.out $i
done

#Using sed:
# sed '/^$/d' input.txt > output.txt

#Using grep:
# grep -v '^$' input.txt > output.txt

#Source: http://www.cyberciti.biz/faq/howto-linux-unix-command-remove-all-blank-lines/
