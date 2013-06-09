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

os.chdir(os.path.realpath(__file__).replace("one_a_day.py", ""))
target_dir = 'papers/'

#Execute

i = 1

ls = os.listdir(os.curdir)
for item in ls:
	if item[-4:] == ".pdf" or item[-4:] == ".PDF":
		filedone = 0
		while filedone == 0:
			toname = datetime.date.today() + datetime.timedelta(days=i)
			toname = toname.strftime("%Y-%b-%d-%a") + ".pdf"

			if os.path.isfile(target_dir + toname):
				i = i + 1
			else:
				shutil.move(item, target_dir + toname)
				filedone = 1


