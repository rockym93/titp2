#!/usr/bin/env python

import titp_write as titp
import cgi
import time

try:
	with open('now.list') as f:
		names = f.readlines()
except IOError:
	names = []

query = cgi.FieldStorage()
names.append(query.getvalue('name'))

timenow = time.gmtime(time.time() + 28800)

daynow = time.strftime('%A', timenow)
hournow = time.strftime('%H', timenow)

for i in names:
	if i in titp.tt[daynow][timenow]:
		titp.tt[daynow][timenow].remove(i)
	titp.tt[daynow][timenow].append(name)
titp.generate()
