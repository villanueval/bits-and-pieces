#!/usr/bin/python
#
# Drop files in a folder to assign to a future date
# One file a day
# I use it to asign reading material
#

# Import modules
import commands
import shutil
import os
import datetime
import random

os.chdir(os.path.realpath(__file__).replace("one_a_day.py", ""))
target_dir = 'papers/'

#Execute

filename_format = "%Y-%b-%d-%a"
i = 0

#Process all pdf files in current dir, give them a future date
ls = os.listdir(os.curdir)
for item in ls:
	if item[-4:] == ".pdf" or item[-4:] == ".PDF":
		if item != "TODAY.pdf":
			filedone = 0
			while filedone == 0:
				toname = datetime.date.today() + datetime.timedelta(days=i)
				toname = toname.strftime(filename_format) + ".pdf"

				if os.path.isfile(target_dir + toname):
					i = i + 1
				else:
					shutil.move(item, target_dir + toname)
					filedone = 1


#Check if there is one for today already, if not get the next one
todayfile = "TODAY.pdf"
if os.path.isfile(todayfile):
	print "File ready"
else:
	i=0
	filedone = 0
	while filedone == 0:
		toname = datetime.date.today() + datetime.timedelta(days=i)
		toname = toname.strftime(filename_format) + ".pdf"

		if os.path.isfile(target_dir + toname):
			print target_dir + toname + "\n"
			shutil.move(target_dir + toname, todayfile)
			filedone = 1
		else:
			i = i + 1


