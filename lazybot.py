#!/usr/bin/env python3
import requests
import sys
import json

key = ''
url = 'https://api.telegram.org/'
commands = {}
handlers = {}

print('Content-Type: application/json')
print('')

data = json.load(sys.stdin)

#with open('key.txt') as f:
#	key = f.read().rstrip()

def api(method, params=None, files=None):
	'''
	I take a Telegram method name, and dictionaries of parameters or files to pass to that method.
	I return a dictionary containing the response.
	'''
	r = requests.post(url + key + '/' + method, params=params, files=files)
	return r.json()
	
def processupdate(update=data):
	'''
	I take an entire (but decoded to dict, please) *update* object from Telegram.
	I look for things that this bot knows how to deal with, and execute the appropriate function.
	'''

	#1. If the update is text, check for commands.
	if 'text' in update['message']:
		text = update['message']['text']
		
		for i in text.split(' '):
			if i[0] == '/':
				cmd = i
				
		if '@' in cmd:
			cmd = cmd.split('@')[0]
		cmd = str(cmd)
		commands[cmd](update['message'])
	
	#2. If the update isn't a command, pass it to the appropriate handler.
	#   This can include a generic text handler
	else:
		for h in handlers:
			if h in update['message']:
				handlers[h](update['message'])

# def getupdates:
# 1. retrieve updates with api(getUpdates)
# 2. for i in updates['result']: processupdate(i)
# 3. repeat? tbd.
