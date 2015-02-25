#!/usr/bin/env python

import titp_write
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
	if i in titp.write.tt[daynow][timenow]:
		titp.write.tt[daynow][timenow].remove(i)
	titp_write.tt[daynow][timenow].append(name)
titp_write.generate()
