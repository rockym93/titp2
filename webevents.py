#!/usr/bin/env python3
import events
import cgi

s = ''

template = '''
<form action="webevents.py" action="POST">
<h4>[{eventid}]</h4>
<p>
<em>{date} - {time}</em><br />
{description}

</p>
<p>
<input type="hidden" name="eventid" value="{eventid}" />
<input type="text" name="name" />
<input class="icon-like" type="submit" name="in" value="&#xe068;" />
<input class="icon-dislike" type="submit" name="out" value="&#xe06d;" />
</p>
</form>
'''

form = cgi.FieldStorage()
rsvpname = form.getvalue('name')
rsvpevent = form.getvalue('eventid')
response = None
if 'in' in form:
	response = True
if 'out' in form:
	response = False

if rsvpname is not None and response is not None:
	events.setattendance(rsvpevent, rsvpname, response)

for eventid in events.listevents():
	event = events.getevent(eventid)
	event['eventid'] = eventid
	event['eventid'] = eventid
	if event['date']:
		event['date'] = "{}/{}/{}".format(*event['date'])
	if event['time']:
		event['time'] = "{}:{}".format(str(event['time'][0]), str(event['time'][1]).zfill(2))

	if len(event['in']) == 0:
		event['in'] = "Nobody is in"
	elif len(event['in']) == 1:
		event['in'] = event['in'][0] + " is in"
	elif len(event['in']) > 1:
		event['in'] = " &".join(", ".join(event['in']).rsplit(",",1)) + " are in"

	if len(event['out']) == 0:
		event['out'] = "Nobody is out"
	elif len(event['out']) == 1:
		event['out'] = event['out'][0] + " is out"
	elif len(event['out']) > 1:
		event['out'] = " &".join(", ".join(event['out']).rsplit(",",1)) + " are out"

	s += template.format(**event)
with open('page.html') as f:
	page = f.read()

print('Content-Type: text/html')
print('')
	
print(page.replace('<!--timetable-->',s))



