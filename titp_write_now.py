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
	if i in titp.tt[daynow][hournow]:
		titp.tt[daynow][hournow].remove(i)
	titp.tt[daynow][hournow].append(i)
titp.generate()

with open('now.list','w') as f:
	f.write(line + '\n' for line in names)
