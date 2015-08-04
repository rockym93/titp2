#!/usr/bin/env python
VERSION = "2.2"
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
			
if 'tz' not in tt.keys():
	tt['tz'] = 0
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
		if i not in string.letters:
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
	timenow = time.gmtime(time.time() + tt['tz'] * 3600)
	daynow = time.strftime('%A', timenow)
	hournow = str(int(time.strftime('%H', timenow))) #We don't want the zero at the front.
	
	if name not in tt['users']:
		tt['users'].append(name)
		
	if daynow in days and hournow in times:	
		if name not in tt[daynow][hournow]:
			tt[daynow][hournow].append(name)
	save()
		
def busynow(name):
	'''Removes a name from the timetable for right now.'''
	timenow = time.gmtime(time.time() + tt['tz'] * 3600)
	daynow = time.strftime('%A', timenow)
	hournow = str(int(time.strftime('%H', timenow))) #We don't want the zero at the front.
	
	if daynow in days and hournow in times:	
		if name in tt[daynow][hournow]:
			tt[daynow][hournow].remove(name)
	save()

def getnow():
	'''Gets who's free right now'''
	timenow = time.gmtime(time.time() + tt['tz'] * 3600)
	daynow = time.strftime('%A', timenow)
	hournow = str(int(time.strftime('%H', timenow))) #We don't want the zero at the front.
	try:
		return tt[daynow][hournow]
	except KeyError:
		return []

def getnext():
	'''Gets who's free next hour'''
	timenow = time.gmtime(time.time() + tt['tz'] * 3600)
	daynow = time.strftime('%A', timenow)
	hournow = str(int(time.strftime('%H', timenow)) + 1)
	try:
		return tt[daynow][hournow]
	except KeyError:
		return []

def gettoday():
	'''Gets who's free for the whole of today.'''
	timenow = time.gmtime(time.time() + tt['tz'] * 3600)
	daynow = time.strftime('%A', timenow)
	try:
		return tt[daynow]
	except KeyError:
		return {}

def generate(): 
	'''Builds the timetable html for all users.'''
	s = str()
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
	print('<html><body>')
	
	processform()
	generate()
	save()

