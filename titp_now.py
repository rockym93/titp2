#!/usr/bin/env python

import time
import json

print('Content-Type: text/plain')
print('')

with open('timetable.json') as f:
	tt = json.load(f)

timenow = time.gmtime(time.time() + 28800)

daynow = time.strftime('%A', timenow)
hournow = str(int(time.strftime('%H', timenow))) #We don't want the zero at the front.

for i in tt[daynow][hournow]:
	print(i)
