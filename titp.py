#!/usr/bin/env python3
VERSION = "3.0"
import cgi
import cgitb
import string
import json
import time
cgitb.enable()

days = ('Monday','Tuesday','Wednesday','Thursday','Friday')
times = ('8','9','10','11','12','13','14','15','16','17','18')

try:
	with open('timetable.json') as f:
		tt = json.load(f)
except IOError:
	tt = {'users':[]}
	for d in days:
		tt[d] = {}
		for h in times:
			tt[d][h] = []
			
try:
	with open('.timezone') as f:
		tz = f.read().rstrip('\n')
except IOError:
	tz = 0

import os
os.environ['TZ'] = tz
time.tzset()
#Defaults to GMT, you'll have to change this in the JSON. Sorry.

def clearname(name):
	'''Removes a name from the timetable'''
	for d in days:
		for h in times:
			if name in tt[d][h]:
				tt[d][h].remove(name)
	if name in tt['users']:
		tt['users'].remove(name)
			
def checks(name, captcha):
	'''Check that CAPTCHA is correct and inputs are safe.'''
	for i in name:
		if i not in string.ascii_letters:
			return False
	if captcha != 'apple':
		return False
	else:
		return True

def processform(): 
	'''This collects the data from the form (add.html)'''
	form = cgi.FieldStorage()
	now = form.getvalue('now')
	if now is not None:
		freenow(now)
	else:
		if form:
			name = str(form.getvalue('name'))
			captcha = str(form.getvalue('captcha'))
			
			if checks(name, captcha):
				clearname(name)
				
				for d in days:
					for h in times:
						if form.getvalue(d + h):
							tt[d][h].append(name)

				tt['users'].append(name)
			else:
				print('Sorry, something bad happened. Check that you answered the spambot question and that your name contains only letters, and try again.')

def freenow(name):
	'''Adds a name to the timetable for right now.'''
	timenow = time.localtime()
	daynow = time.strftime('%A', timenow)
	hournow = str(timenow.tm_hour)
	
	if name not in tt['users']:
		tt['users'].append(name)
		
	if daynow in days and hournow in times:	
		if name not in tt[daynow][hournow]:
			tt[daynow][hournow].append(name)
	save()
		
def busynow(name):
	'''Removes a name from the timetable for right now.'''
	timenow = time.localtime()
	daynow = time.strftime('%A', timenow)
	hournow = str(timenow.tm_hour)
	
	if daynow in days and hournow in times:	
		if name in tt[daynow][hournow]:
			tt[daynow][hournow].remove(name)
	save()

def getnow():
	'''Gets who's free right now'''
	timenow = time.localtime()
	daynow = time.strftime('%A', timenow)
	hournow = str(timenow.tm_hour)
	try:
		return tt[daynow][hournow]
	except KeyError:
		return []

def getnext():
	'''Gets who's free next hour'''
	timenow = time.localtime()
	daynow = time.strftime('%A', timenow)
	hournow = str(timenow.tm_hour + 1)
	try:
		return tt[daynow][hournow]
	except KeyError:
		return []

def gettoday():
	'''Gets who's free for the whole of today.'''
	timenow = time.localtime()
	daynow = time.strftime('%A', timenow)
	try:
		return tt[daynow]
	except KeyError:
		return {}

def generate(): 
	'''Builds the timetable html for all users.'''
	s = str()
	s +=  '<p><a href="add.html">Add or modify availability</a></p>\n'
	s +=  '<p>Currently tracking ' + str(len(tt['users'])) + ' people\'s availability between classes.</p>\n\n'
	s +=  '<div style="padding:1em"><table style="width:100%" border="1">\n<tr><td></td><td>Monday</td><td>Tuesday</td><td>Wednesday</td><td>Thursday</td><td>Friday</td></tr>\n'
	
	for h in times:
		s +=  "<tr><td>" + str(h) + '</td>'
		for d in days:
			s += '<td>'
			for i in tt[d][h]:
				s += i + '<br />'
			s += '</td>'
		s += '</tr>\n'
	
	s +=  '<form method="post" action="titp.py"><p>Hello! My name is <input type="text" name="name" /> and I am free <input type="submit" value="right now!" /></p></form>'
	s +=  '</table></div>\n<p>Generated by TITP Version ' + VERSION + '</p>'
	
	
	with open('page.html') as f:
		page = f.read()
	
	print(page.replace('<!--timetable-->',s))


def save():
	'''Saves internal timetable state.'''
	with open('timetable.json','w') as f:
		json.dump(tt,f)

if __name__ == '__main__':
	
	print('Content-Type: text/html')
	print('')

	
	processform()
	generate()
	save()

