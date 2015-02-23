#!/usr/bin/env python
VERSION = "0.3"
import sys
import os
import cgi
import datetime
import cgitb
cgitb.enable()

DAYS = ('MO','TU','WE','TH','FR')
TIMES = ('8','9','10','11','12','13','14','15','16','17','18')
HUMANDAYS = {'MO':'Monday','TU':'Tuesday','WE':'Wednesday','TH':'Thursday','FR':'Friday'}
DATETIMEDAYS = {0:"MO",1:"TU",2:"WE",3:"TH",4:"FR",5:"MO",6:"MO"}
CAL = dict()
USERS = os.listdir('data')

#Set up the main dict with list objects for each day and time.
for day in DAYS:
	for time in TIMES:
		CAL[day+time] = list()

#This populates the main dict from the filesystem.
def slurp(): #Pardon my whimsical function name. 
	for user in USERS:
		for day in DAYS:
			for time in TIMES:
				f = open('data/' + user + '/' + day + '/' + time)
				CAL[day+time].append(f.read())
				f.close()
			
#def savetofile():
#	for day in DAYS:
#		for time in TIMES:
#			s = CAL[day+time]
#			f = open(day + '/' + time, 'w')
#			f.writelines(s)
#			f.close()

slurp()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print "<html>"
print "<head><title>The Inverse Timetable Project - ONE DAY VIEW</title></head>"
print "<body>"
print '<b>Today\'s Inversed Timetable.</b> <a href="index.shtml">Back to full view.</a>'
print "<table border=1><tr><td></td><td>8AM</td><td>9AM</td><td>10AM</td><td>11AM</td><td>12PM</td><td>1PM</td><td>2PM</td><td>3PM</td><td>4PM</td><td>5PM</td><td>6PM</td></tr>"
#print "<h2>The Inverse Timetable Project</h2><h3>Currently showing " + str(len(USERS)) + " people's avaliability between classes.</h3>"
#print '<a href="add.html">Add your inversed timetable here.</a><br><br>'



currentday = datetime.date.today()
day = DATETIMEDAYS[currentday.weekday()]
print "<tr><td>"
print HUMANDAYS[day]
print "</td>"
for time in TIMES:
	print "<td>"
	for entry in CAL[day+time]:
		if entry:
			print entry + '<br>'
	print "</td>"
print "</tr>"
print "</table>"

print '<br>Key:'
for user in USERS:
	print "<br>"
	f = open('data/' + user + '/name')
	print '<a href=data/' + user + '>' + user + '</a>'
	print f.read()
	f.close()
	

print '<br><br>titp.py version ' + VERSION
print "</body></html>"
