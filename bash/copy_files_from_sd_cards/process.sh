#!/bin/bash
#
dep=$1

mount /mnt/flash1
sleep 5
mount /mnt/flash2
sleep 5

cd
cd sounds
mkdir $dep

cd $dep

cp /mnt/flash1/Data/* .
cp /mnt/flash2/Data/* .

umount /mnt/flash1
umount /mnt/flash2

cd ../

#beep -f 1000 -n -f 2000 -n -f 1500

met=`df | awk '/meeting/ {print $3}'`

if [ $met -gt "40000000" ]
then
  #rsync -ruh $dep /mnt/meeting/
  cp -r $dep /mnt/meeting/
  #rm -r $dep
else
  mkdir 2move
  mv $dep 2move
fi  

beep -f 1000 -n -f 2000 -n -f 1500

cd

