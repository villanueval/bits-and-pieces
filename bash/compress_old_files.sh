#!/bin/bash
#
#Bash script to compress files older than "daysold" number of days
# in the directory "logdir".
# Useful for log directories.
#From http://unix.stackexchange.com/a/58757
#

$daysold=3
$logdir="/home/user/logs/"


#compress
find $logdir -mtime +$daysold | xargs  tar -czvPf  $logdir/logs_$(date +%F).tar.gz

#delete
find $logdir -mtime +$daysold | xargs  -n1 echo rm
