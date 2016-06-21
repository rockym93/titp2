#!/usr/bin/env python3
import events
import cgi

s = '''
<p>
<a href="javascript:void(0)" onclick="document.getElementById('newevent').style.display='block'"><span class="icon-plus"></span>create event</a>
</p>
<div id="newevent" style="margin:1em; display:none">

<form method="post" action="webevents.py">
<p>
event id: <input type="text" name="newid" value=""/><br />
date: <input type="text" name="newdate" value="dd/mm/yyyy"/><br />
time: <input type="text" name="newtime" value="hh:mm"/><br />
description:<br />
<textarea rows="12" cols="40" name="newdesc"></textarea><br /><br />
<input type="submit" value="Post" /><br />
</p>
</form>
</div>
'''

template = '''
<form action="webevents.py" action="POST">
<h4>[{eventid}]</h4>
<p>
<em>{date} - {time}</em><br />
{description}
</p>
<p>{in}</p>
<p>{out}</p>
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
	
if 'newid' in form:
	newid = form.getvalue('newid')
	newdate = form.getvalue('newdate')
	newtime = form.getvalue('newtime')
	newdesc = form.getvalue('newdesc')

	events.newevent(newid)
	if newdate is not 'dd/mm/yyyy':
		events.setdate(newid, newdate)
	if newtime is not 'hh:mm':
		events.settime(newid, newtime)
	if newdesc is not None:
		events.setdescription(newid, newdesc)

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



