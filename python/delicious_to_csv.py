#!/usr/bin/python
# v. 3 feb 2013
"""
Script to export the bookmarks form delicious export file to 2 csv files.
  This eases importing them to a database.
"""

userid='ljvillanueva'

#########################################################################
# EXECUTE THE SCRIPT							#
#########################################################################

ins = open( "delicious.html", "r" )
delicious = []
for line in ins:
    delicious.append( line )

del delicious[0:8]

del delicious[-1]

i=100

delicious2 = []

for bookmark in delicious:
	if bookmark.startswith("<DT>"):
		bookmark = bookmark.replace( "|", "-" )
		delicious2.append(bookmark.replace( "<DT><A HREF=\"", str(i) + "|\"" ))
		i += 1

delicious3 = []

for bookmark in delicious2:
	delicious3.append(bookmark.replace( "\" ADD_DATE=\"", "\"|\"" ))


delicious4 = []

for bookmark in delicious3:
	delicious4.append(bookmark.replace( "\" PRIVATE=\"", "\"|\"" ))

delicious5 = []

for bookmark in delicious4:
	delicious5.append(bookmark.replace( "\" TAGS=\"", "\"|\"" ))

delicious6 = []

for bookmark in delicious5:
	delicious6.append(bookmark.replace( "\">", "\"|\"" ))

delicious7 = []

for bookmark in delicious6:
	delicious7.append(bookmark.replace( "</A>", "\"" ))


f = open("bookmarks.csv", 'w')
f1 = open("tags.csv", 'w')

f.write("\"id\",\"url\",\"title\",\"user_id\",\"public\",\"added\",\"lastmodified\",\"clickcount\"\n")
f1.write("\"bookmark_id\",\"tag\"\n")

for bookmark in delicious7:
	bookmark = bookmark.replace( "\n", "")
	bookmark = bookmark.split("|")
	f.write(str(bookmark[0]) + "," + bookmark[1] + "," + bookmark[5] + ',' + userid + ",0," + bookmark[2] + "," + bookmark[2] + ",0\n")
	tags = bookmark[4].split(",")
	for tag in tags:
		tag = tag.replace( "\"", "")
		f1.write(str(bookmark[0]) + ",\"" + tag + "\"\n")

f.close()
f1.close()

