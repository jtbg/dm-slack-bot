import codecs
import csv
import json
import requests
from contextlib import closing
from flask import jsonify
from fuzzywuzzy import fuzz, process


with open('config.json', 'r') as jsonfile:
	jsondata = jsonfile.read()
config = json.loads(jsondata)


def verify_web_hook(form):
	if not form or form.get('token') != config['SLACK_TOKEN']:
		raise ValueError('Invalid request/credentials.')

#convert responses to a reasonably-formatted slack message
def format_slack_message(response, query=None):
	message = {
	'response_type': 'in_channel',xp
	'attachments': []
	}

	attachment = {}
	attachment['color'] = '#3367d6'
	attachment['title'] = response['title']
	attachment['text'] = response['text']

	message['attachments'].append(attachment)

	return message

# functions to read from the CSVs and build responses

def read_tldr(session_date=None):
	response = {}
	response['title'] = "TL;DR"
	url = config['TLDR_CSV']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			if session_date == row[0]:
				response['text'] = row[1]
		response['text'] = row[1]
		return response	

def read_xp():
	response = {}
	url = config['LOG_CSV']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			xp = row[10]
			level = row[11]
			needed = row[12]
		response['title'] = 'Current XP'
		response['text'] = "The party's current XP is {}, putting you at level {}. You need {}xp more to level up".format(xp, level, needed)
		return response

def read_whois(npc_name='list'):
	response = {}
	response['text'] = ''
	npcs = {}
	url = config['WHOIS_CSV']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			name = row[0]
			description = row[1]
			npcs[name] = description
		if npc_name.lower() == 'list':
			response['title'] = 'List of NPCs'
			for npc_name in list(npcs.keys()):
				response['text'] = response['text'] + '\n' + npc_name
			return response
		search_match = process.extractOne(npc_name, list(npcs.keys()))
		response['title'] = search_match[0]
		response['text'] = npcs[search_match[0]]
		return response

# define the functions that will be available for slash commands

def xp(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405
	
	verify_web_hook(request.form)
	msg_to_send = format_slack_message(read_xp())
	return jsonify(msg_to_send)

def tldr(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405

	verify_web_hook(request.form)
	msg_to_send = format_slack_message(read_tldr())
	return jsonify(msg_to_send)

def whois(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405

	verify_web_hook(request.form)
	msg_to_send = format_slack_message(read_whois(request.form['text']))
	return jsonify(msg_to_send)
