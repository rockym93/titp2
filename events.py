#!/usr/bin/env python3
import json
import time
try:
	with open('.timezone') as f:
		tz = f.read().rstrip('\n')
except IOError:
	tz = '0'

import os
os.environ['TZ'] = tz
time.tzset()

now = time.localtime()

try:
	with open('events.json') as f:
		events = json.load(f)
except IOError:
	events = {}
	
def save():
	with open('events.json', 'w') as f:
		json.dump(events, f)

	

def newevent(eventid, 
	date=None, 
	time=None, 
	location=None, 
	description=None, 
	new=True,
	visible=True):
	
	events[eventid] = {'date':date,
		'time':time, 
		'location':location, 
		'description':description, 
		'new':new,
		'visible':visible,
		'in':[],
		'out':[]}
	save()
	
def	setdate(eventid, datestring):
	if datestring.lower() == 'today':
		datesplit = [now.tm_mday, now.tm_mon, now.tm_year]
	elif datestring.lower() == 'tomorrow':
		datesplit = [now.tm_mday + 1, now.tm_mon, now.tm_year]
	else:
		datesplit = datestring.split('/')
		if len(datesplit) == 1:
			datesplit.append(now.tm_mon)
		if len(datesplit) == 2:
			datesplit.append(now.tm_year)
	datesplit = [int(x) for x in datesplit]
	events[eventid]['date'] = datesplit
	save()


def settime(eventid, timestring):
	pm = None
	if 'am' in timestring.lower():
		pm = False
		timestring = timestring.lower().replace('am','')
	if 'pm' in timestring.lower():
		pm = True
		timestring = timestring.lower().replace('pm','')
		
	timesplit = timestring.split(':')
	timesplit = [int(x) for x in timesplit]
	
	if len(timesplit) == 1:
		timesplit.append(00)
	if len(timesplit) > 2:
		timesplit = [ timesplit[0], timesplit[1] ]
		
	if pm is None:
		if 7 < timesplit[0] < 12:
			pm = False
		else:
			pm = True
	
	if pm and timesplit[0] is not 12:
		timesplit[0] = timesplit[0] + 12
	
	events[eventid]['time'] = timesplit
	save()


def setlocation(eventid, location):
	if type(location) == str:
		location = location.split(',')
	location = [float(x) for x in location]
	events[eventid]['location'] = location
	save()

def setdescription(eventid, description):
	events[eventid]['description'] = description
	save()
	
def listevents():
	return events.keys()
	
def getevent(eventid):
	try:
		return events[eventid]
	except KeyError:
		return None
		
def setattendance(eventid, person, attending):
	if attending and person not in events[eventid]['in']:
		events[eventid]['in'].append(person)
		try:
			events[eventid]['out'].remove(person)
		except ValueError:
			pass
	elif not attending and person not in events[eventid]['out']:
		events[eventid]['out'].append(person)
		try:
			events[eventid]['in'].remove(person)
		except ValueError:
			pass
	save()

def deleteevent(eventid):
	del events[eventid]
	save()
