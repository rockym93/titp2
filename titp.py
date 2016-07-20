#!/usr/bin/env python3
VERSION = "3.1a"

import json
import time

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
	tz = 'UTC'ti

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

def save():
	'''Saves internal timetable state.'''
	with open('timetable.json','w') as f:
		json.dump(tt,f)

