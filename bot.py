#!/usr/bin/env python

import titp
import sys
import json
import lazybot as bot

print('Content-Type: application/json')
print('')

data = json.load(sys.stdin)

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
		t = free[0] + " is free right now."
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
		t = free[0] + " is free next hour."
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
		for hour in free:
			names = ''
			if len(hour) == 0:
				pass
			if len(hour) == 1:
				names = hour[0]
			else:
				for i in hour:
					if hour.index(i) == len(hour)-1:
						names += "& "
						names += i
					elif hour.index(i) == len(hour)-2:
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
I am a frontend to The Inverse Timetable Project at https://www.rockym93.net/code/titp2/ .

/start sets you up to use me.
/callme changes the name I - and the website - use for you.
/free marks you as free at this time - permanently.
/busy marks you as busy at this time - permanently.
/now tells you who is free right now.

I am a shy bot! I prefer to make changes in private chats.
I am a bit of a beta! Please report bugs to @rockym93.'''
	send = { 'text': t, 'chat_id': chat_id }
	bot.api('sendMessage', send)

bot.commands['/help'] = halp

def echo(message):
	from_id = message['from']['id']
	if from_id == config['admin']:
		chat_id = message['text'].split(' ', 2)[1]
		t = message['text'].split(' ', 2)[2]
		send = { 'text': t, 'chat_id': chat_id }
		bot.api('sendMessage', send)

bot.commands['/echo'] = echo

### End Definitions ###

bot.processupdate(data)
