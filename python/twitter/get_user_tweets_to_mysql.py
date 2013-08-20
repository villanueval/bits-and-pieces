#!/usr/bin/python

#To avoid unicode problems
# from http://pythonadventures.wordpress.com/2012/09/02/print-unicode-text-to-the-terminal/
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#which users to get the timeline?
users = ['', '']

#Twitter API
c_key = ''
c_secret = ''
atoken_key = ''
atoken_secret = ''

#MySQL
db_hostname=""
db_username=""
db_password=""
db_database=""
thistable=""

#Functions

def insertTL(thisid, thisuser, created_at, created_at_s, in_reply, location, thistext, retweets):
	#Open MySQL
	try:
		con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database, charset='utf8', init_command='SET NAMES UTF8')
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit (1)
	cursor = con.cursor()
	#query = 'INSERT INTO ' + thistable + ' (thisuser, thisid, created_at, created_at_s, in_reply, location, thistext, retweets) VALUES (' + \
	#	`thisuser` + ', ' + `created_at` + ', ' + `created_at_s` + ', ' + `in_reply` + ', ' + `location` + ', ' + `thistext` + ', ' + `retweets` + ')'
	#print "Query: " + query + "\n"
	#cursor.execute(query)
	#From http://stackoverflow.com/a/6203782
	#print thisid + "\n"
	cursor.execute(u"REPLACE INTO " + thistable + " (thisuser, thisid, created_at, created_at_s, in_reply, location, thistext, retweets) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (thisuser, thisid, created_at, created_at_s, in_reply, location, thistext, retweets))
	con.commit()
	#Close MySQL
	cursor.close()
	con.close()
	return

#Start

#Python script to get the timeline of a user.
# Uses the python-twitter module (https://github.com/bear/python-twitter)
#
import twitter
import time
import MySQLdb

api = twitter.Api(input_encoding = 'utf-8')

api = twitter.Api(consumer_key=c_key, consumer_secret=c_secret, access_token_key=atoken_key, access_token_secret=atoken_secret)


for thisuser in users:
	done=0
	maxst_id = ''
	
	while done==0:

		limit = api.GetRateLimitStatus()

		thislimit = limit['resources']['statuses']['/statuses/user_timeline']['remaining']
	
		print "\n Twitter limit: " + str(thislimit)
	
		if thislimit < 50:
			print "\n\n Approaching limit, waiting one hour...\n"
			time.sleep(3600)
	
		statuses = api.GetUserTimeline(screen_name=thisuser, include_rts="TRUE", count=200, max_id=maxst_id)

		maxst_id = 1000000000000000000000000000

		if len(statuses) == 0:
			done=1
			#sys.exit("Nothing more")

		#statusFile = open(thisuser + ".csv", "a")

		print "\n Found " + str(len(statuses)) + "tweets by " + thisuser 

		for i in range(1, len(statuses)):
	
			#statuses[1].text
			#statuses[1].id
			thistext = statuses[i].text.replace('\n', ' ').decode('utf8')
			thisid = str(statuses[i].id)
			created_at = str(statuses[i].created_at)
			created_at_s = str(statuses[i].created_at_in_seconds)
			if statuses[i].in_reply_to_screen_name is None:
				in_reply = ""
			else:
				in_reply = str(statuses[i].in_reply_to_screen_name)
			if statuses[i].location is None:
				location = ""
			else:
				location = str(statuses[i].location)
			retweets = str(statuses[i].retweet_count)
			
			#statusFile.write(thisid + '\t' + created_at + '\t' + created_at_s + '\t' + in_reply + '\t' + location + '\t' + thistext + '\t' + retweets + '\n')
			insertTL(thisid, thisuser, created_at, created_at_s, in_reply, location, thistext, retweets)
			if maxst_id > statuses[i].id:
				maxst_id = statuses[i].id
			
			#print ".",
		#statusFile.close()
		print "\n Waiting a few seconds..."
		time.sleep(5)
		
