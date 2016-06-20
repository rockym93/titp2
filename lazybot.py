#!/usr/bin/env python3
import requests
import sys
import json

key = ''
url = 'https://api.telegram.org/'
commands = {}
handlers = {}
logging = False

print('Content-Type: text/html')
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
	if logging:
		with open('dump.json','a') as f:
			json.dump(update,f)
	
	#0. First, check for callback queries
	if 'callback_query' in update:
		if 'callback_query' in handlers:
			handlers['callback_query'](update['callback_query'])
	
	#1. If the update is text, check for commands.
	elif 'message' in update:
		try:
			text = update['message']['text']
			cmd = text.split(' ')[0]
		
			if '@' in cmd:
				cmd = cmd.split('@')[0]
			
			commands[cmd](update['message'])
			
		#2. If the update isn't a text command in our command list, 
		#   pass it to the appropriate handler.
		#   This can include a generic text handler
		
		except KeyError:
			for h in handlers:
				if h in update['message']:
					handlers[h](update['message'])
		




# def getupdates:
# 1. retrieve updates with api(getUpdates)
# 2. for i in updates['result']: processupdate(i)
# 3. repeat? tbd.
