#!/bin/bash
# Script to export the pumilio git archive to several installations in the server and update it using wget

mkdir 1
cp -r pumilio/www/* 1/

rm -r 1/install
rm -r 1/tmp
rm -r 1/sounds

for site in site1 site2 site3
do
  cp -rf 1/* /var/www/$site/
  wget -O /dev/null http://localhost/$site/upgrade
done

rm -r 1
