#!/usr/bin/python

# Import modules
from subprocess import call
import sys
import time

#Call the script giving one arguments
steps=int(sys.argv[1])
end=int(sys.argv[2])



##########################################################
# RUN
##########################################################

start = 1

while (start < end):
	for i in range(start, start + steps):
		print "WinHPC_XMLCreator_Minutes_Local.py " + str(start) + " " + str(start + steps)
		call(["./WinHPC_XMLCreator_Minutes_Local.py", str(start), str(start + steps)])
		start = start + steps
		time.sleep(4)
