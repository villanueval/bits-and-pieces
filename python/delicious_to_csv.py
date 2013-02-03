#!/usr/bin/python
# v. 3 feb 2013
"""
Script to export the bookmarks form delicious export file to 2 csv files.
  This eases importing them to a database.
"""

userid=''

#if you want to avoid a tag
tag_to_avoid=''

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

if tag_to_avoid != '':
	for bookmark in delicious2:
		if bookmark.find( tag_to_avoid ) == -1:
			delicious3.append(bookmark)
else:
	delicious3 = delicious2

delicious4 = []

for bookmark in delicious3:
	delicious4.append(bookmark.replace( "\" ADD_DATE=\"", "\"|\"" ))

delicious5 = []

for bookmark in delicious4:
	delicious5.append(bookmark.replace( "\" PRIVATE=\"", "\"|\"" ))

delicious6 = []

for bookmark in delicious5:
	delicious6.append(bookmark.replace( "\" TAGS=\"", "\"|\"" ))

delicious7 = []

for bookmark in delicious6:
	delicious7.append(bookmark.replace( "\">", "\"|\"" ))

delicious8 = []

for bookmark in delicious7:
	delicious8.append(bookmark.replace( "</A>", "\"" ))

f = open("bookmarks.csv", 'w')
f1 = open("tags.csv", 'w')

f.write("\"id\",\"url\",\"title\",\"user_id\",\"public\",\"added\",\"lastmodified\",\"clickcount\"\n")
f1.write("\"bookmark_id\",\"tag\"\n")

for bookmark in delicious8:
	bookmark = bookmark.replace( "\n", "")
	bookmark = bookmark.split("|")
	f.write(str(bookmark[0]) + "," + bookmark[1] + "," + bookmark[5] + ',' + userid + ",0," + bookmark[2] + "," + bookmark[2] + ",0\n")
	tags = bookmark[4].split(",")
	for tag in tags:
		tag = tag.replace( "\"", "")
		tag = tag.replace( " ", "")
		f1.write(str(bookmark[0]) + ",\"" + tag + "\"\n")

f.close()
f1.close()

