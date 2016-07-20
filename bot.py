#!/usr/bin/env python3

import sys
import json
import lazybot as bot

try:
	with open('bot.json') as f:
		config = json.load(f)
except IOError:
	config = {
	'admin':None,
	'key':None,
	'users': {},
	'ping': []
	}

bot.key = config['key']
bot.logging = True

def save_config():
	with open('bot.json','w') as f:
		json.dump(config, f)

### Command Definitions ###

def start(message):
	from_id = message['from']['id']
	firstname = message['from']['first_name']
	t = "Hello!\n"

#	t += "It looks like you're a new bot user. "
	if firstname in titp.tt['users']:
		t += "It looks like you're already using TITP under your first name.\n"
		t += "If that's not the case, you'll need to choose an alias using /callme, followed by your name."
	if firstname not in titp.tt['users']:
		t += "It looks like you're a new TITP user\n"
		t += "If you're already using TITP on the web, you can fix this by typing /callme, followed by the name you use on TITP.\n"
		t += "If not, you'll be registered the first time you change your availabilities."
	send = { 'text': t, 'chat_id': from_id }
	bot.api('sendMessage', send)
	

bot.commands['/start'] = start

def callme(message):
	from_id = message['from']['id']
	firstname = message['from']['first_name']
	newname = message['text'].split(' ')[-1]
	config['users'][from_id] = newname
	send = { 'text': 'Okay, ' + newname + ' it is.', 'chat_id': from_id }
	bot.api('sendMessage', send)
	
	save_config()
	
bot.commands['/callme'] = callme

def now(message):
	chat_id = message['chat']['id']
	free = titp.getnow()
	if len(free) == 0:
		t = "Nobody is free right now."
	elif len(free) == 1:
		t = free[0] + " is lonely right now."
	else:
		t = ""
		for i in free:
			if free.index(i) == len(free)-1:
				t += "and "
				t += i
			elif free.index(i) == len(free)-2:
				t += i
				t += " "
			else:
				t += i
				t += ", "
		t += " are free right now."
	send = { 'text': t, 'chat_id': chat_id }
	bot.api('sendMessage', send)
	
bot.commands['/now'] = now
	
def next_now(message): #avoiding collision with next keyword; command is /next.
	chat_id = message['chat']['id']
	free = titp.getnext()
	if len(free) == 0:
		t = "Nobody is free next hour."
	elif len(free) == 1:
		t = free[0] + " is lonely next hour."
	else:
		t = ""
		for i in free:
			if free.index(i) == len(free)-1:
				t += "and "
				t += i
			elif free.index(i) == len(free)-2:
				t += i
				t += " "
			else:
				t += i
				t += ", "
		t += " are free next hour."
	send = { 'text': t, 'chat_id': chat_id }
	bot.api('sendMessage', send)
	
bot.commands['/next'] = next_now

def today(message):
	chat_id = message['chat']['id']
	free = titp.gettoday()
	template = "[{hour}]: {names}\n"

	if free:
		t = "Today's timetable:\n\n"
		for hour in titp.times:
			names = ''
			if len(free[hour]) == 0:
				pass
			if len(free[hour]) == 1:
				names = free[hour][0]
			else:
				for i in free[hour]:
					if free[hour].index(i) == len(free[hour])-1:
						names += "& "
						names += i
					elif free[hour].index(i) == len(free[hour])-2:
						names += i
						names += " "
					else:
						names += i
						names += ", "
			t += template.format(hour=hour, names=names)
	else:
		t = "Today's availabilities are not... available. How ironic. It's probably the weekend, go outside or something."
	send = { 'text': t, 'chat_id': chat_id }
	bot.api('sendMessage', send)

bot.commands['/today'] = today
					
			

def free(message):
	from_id = message['from']['id']
	username = message['from']['first_name']
	if str(from_id) in config['users']:  #str() because json uses string keys
		username = config['users'][from_id]	
	titp.freenow(username)

bot.commands['/free'] = free

def busy(message):
	from_id = message['from']['id']
	username = message['from']['first_name']
	if str(from_id) in config['users']:
		username = config['users'][from_id]
	titp.busynow(username)
		
bot.commands['/busy'] = busy

def halp(message):
# to be mapped to /help, but we're avoiding a collision with the builtin.
	chat_id = message['chat']['id']
	t = '''
I am a frontend to [The Inverse Timetable Project](https://www.rockym93.net/code/titp2/).

*Timetabling*
/free marks you as free at this time - permanently.
/busy marks you as busy at this time - permanently.
/now tells you who is free right now.
/next tells you who is free next.
/today tells you who is free all day.

*Events*
/new (eventname) creates a new event.
/set (eventname) (time/date/description/location) (new detail to set) sets details.
/end (eventname) removes an event.
/list will tell you which events are coming up.
/info (eventname) will tell you more and let you RSVP.'''
	send = { 'text': t, 'chat_id': chat_id, 'parse_mode':'Markdown' }
	bot.api('sendMessage', send)

bot.commands['/help'] = halp

def echo(message):
	from_id = message['from']['id']
	if from_id == config['admin']:
		chat_id = message['text'].split(' ', 2)[1]
		t = message['text'].split(' ', 2)[2]
		send = { 'text': t, 'chat_id': chat_id, 'reply_markup': '{"hide_keyboard": true}'}
		bot.api('sendMessage', send)

bot.commands['/echo'] = echo

### Event management ###
import events

def newevent(message):
	chat_id = message['chat']['id']
	from_id = message['from']['id']
	t = message['text'].split(' ',4)
	try:
		eventid = t[1].lower()
	except IndexError:
		send = {'text': "You need to specify a name for your event. Try /new (eventname) instead.", 'chat_id': chat_id}
		bot.api('sendMessage', send)
	else:
		send = {'text':"",'chat_id': chat_id,}
		problems = False
		events.newevent(eventid)
		if len(t) >= 3:
#			try:
			events.setdate(eventid, t[2])
#			except:
#				send['text'] += "Theres a problem with your date.\n"
#				problems = True
		if len(t) >=4:
#			try:
			events.settime(eventid, t[3])
#			except:
#				send['text'] += "There's a problem with your time.\n"
#				problems = True
		if len(t) >= 5:
#			try:
			events.setdescription(eventid, t[4])
#			except:
#				send['text'] += "There's a problem with your description.\n"
#				problems = True

		if problems:
			send['text'] += "Apart from that... "
		send['text'] += "Your event has been created!"
		bot.api('sendMessage', send)

bot.commands['/new'] = newevent

def setevent(message):
	chat_id = message['chat']['id']
	t = message['text'].split(' ',3)
	usage = "This works like this: /set [event name] [thing you want to change] [what you want to change it to]"
	dateusage = "Date: Today, tomorrow, 26, 26/1 or 26/1/2016 are all ok."
	timeusage = "Time: 11am 11pm or 11:37 are all ok"
	locusage = "Location: reply to this message with a location attachment."
	descusage = "Description: Go nuts - but it can't be empty."
	hideusage = "Hidden: Use 'hidden' or 'visible' to set whether the event shows in listings."
	try:
		eventid = t[1].lower()
		attribute = t[2].lower()
	except IndexError:
		bot.api('sendMessage', { 'text': usage, 'chat_id': chat_id })
	else:

		if attribute in 'date':
			try:
				events.setdate(eventid, t[3])
			except:
				bot.api('sendMessage', { 'text': dateusage, 'chat_id': chat_id })
		
		if attribute in 'time':
			try:
				events.settime(eventid, t[3])
			except:
				bot.api('sendMessage', { 'text': timeusage, 'chat_id': chat_id })

		if attribute in 'description':
			try:
				events.setdescription(eventid, t[3])
			except:
				bot.api('sendMessage', { 'text': descusage, 'chat_id': chat_id })

		
		if attribute in 'location':
			with open('locodex.json') as f:
				locodex = json.load(f)
			if len(t) == 4:
				if t[3] in locodex:
					events.setlocation(eventid, locodex[location])
			else:
				bot.api('sendMessage', 
				{ 'text': "[" + eventid + "]\n" + locusage, 
				'chat_id': chat_id, 
				'reply_to_message_id':message['message_id'],
				'reply_markup': '{"force_reply": true, "selective": true}'
				})
		if attribute in 'hidden':
			try:
				events.setvisible(eventid, False)
			except:
				bot.api('sendMessage', { 'text': hideusage, 'chat_id': chat_id })

		if attribute in 'visible':
			try:
				events.setvisible(eventid, True)
			except:
				bot.api('sendMessage', { 'text': hideusage, 'chat_id': chat_id })



bot.commands['/set'] = setevent

	
def locationhandler(message):
	eventid = message['reply_to_message']['text'].split(']')[0].lstrip('[').lower()
	location = (message['location']['latitude'], message['location']['longitude'])
	events.setlocation(eventid, location)
	
bot.handlers['location'] = locationhandler

def listevents(message):
	t = { 'chat_id': message['chat']['id'], 'text':"*Current events:*\n",'parse_mode':'Markdown','reply_markup': '{"hide_keyboard": true}'}
	for i in events.listevents():
		event = events.getevent(i)
		#~ try:
			#~ edate = "{}/{}/{}".format(*event['date'])
		#~ except KeyError:
			#~ edate = "no date set,"
		#~ try:
			#~ etime = "{}:{}".format(*event['time'])
		#~ except KeyError:
			#~ etime = "no time set"

		t['text'] += i + "\n"
	bot.api('sendMessage', t)

bot.commands['/list'] = listevents

def detailbuilder(eventid):
	template = '''*[{eventid}]*
_{date} {time}_
{description}

{in}

{out}
'''
	event = events.getevent(eventid)
	event['eventid'] = eventid
	if event['date']:
		event['date'] = "{}/{}/{}".format(*event['date'])
	if event['time']:
		event['time'] = "{}:{}".format(str(event['time'][0]), str(event['time'][1]).zfill(2))
#	event['in'] = "\n".join(event['in'])
#	event['out'] = "\n".join(event['out'])
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

	
	for i in event:
		if not event[i]:
			event[i] = ""
	return template.format(**event)
	
def eventdetails(message):

	
	eventid = message['text'].split(' ')[1].lower()
	event = events.getevent(eventid)

	if event['location']:
		l = { 'chat_id': message['chat']['id'], 
		'latitude': event['location'][0],
		'longitude': event['location'][1]}
		bot.api('sendLocation',l)
	t = { 'chat_id': message['chat']['id'], 
	'text': detailbuilder(eventid),
	'parse_mode':'Markdown',
	'reply_markup': '{"inline_keyboard": [[{"text": "\\ud83d\\udc4d", "callback_data": "1 ' + eventid +'"},{"text": "\\ud83d\\udc4e", "callback_data": "0 ' + eventid +'"}]]}'}
	bot.api('sendMessage', t)
	

bot.commands['/info'] = eventdetails

def attendhandler(message):
	user = message['from']['first_name']
	state = message['data'].split(' ')[0]
	eventid = message['data'].split(' ')[1].lower()
	originator = message['message']

	
	print([eventid, user, state], file=sys.stderr)
	if state == "1": 
		events.setattendance(eventid, user, True)

	elif state == "0": 
		events.setattendance(eventid, user, False)

	
	e = {'chat_id':originator['chat']['id'],
	'message_id':originator['message_id'],
	'text': detailbuilder(eventid),
	'parse_mode':'Markdown',
	'reply_markup': '{"inline_keyboard": [[{"text": "\\ud83d\\udc4d", "callback_data": "1 ' + eventid +'"},{"text": "\\ud83d\\udc4e", "callback_data": "0 ' + eventid +'"}]]}'}
	
	bot.api('editMessageText', e)
		
	

bot.handlers['callback_query'] = attendhandler

def deleteevent(message):
	eventid = message['text'].split(' ')[1]
	events.deleteevent(eventid)

bot.commands['/end'] = deleteevent


## End Definitions ###

bot.processupdate(bot.data)
