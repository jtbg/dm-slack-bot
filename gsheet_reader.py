import codecs
import csv
import requests
from contextlib import closing
from fuzzywuzzy import fuzz, process

with open('config.json', 'r') as jsonfile:
	jsondata = jsonfile.read()
config = json.loads(jsondata)

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
		

def current_xp():
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

def whois(npc_name='list'):
	response = {}
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