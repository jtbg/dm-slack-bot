import gsheet_reader
import json
from flask import jsonify

with open('config.json', 'r') as jsonfile:
	jsondata = jsonfile.read()
config = json.loads(jsondata)


def verify_web_hook(form):
	if not form or form.get('token') != config['SLACK_TOKEN']:
		raise ValueError('Invalid request/credentials.')

def format_slack_message(query=None, response):
	message = {
	'response_type': 'in_channel',
	'text': 'Query: {}'.format(query),
	'attachments': []
	}

	attachment = {}
	attachment['color'] = '#3367d6'
	attachment['title'] = response['title']
	attachment['text'] = response['text']

	message['attachments'].append(attachment)

	return message

def xp(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405
	
	verify_web_hook(request.form)
	msg_to_send = format_slack_message(gsheet_reader.current_xp())
	return jsonify(msg_to_send)

def tldr(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405

	verify_web_hook(request.form)
	msg_to_send = format_slack_message(gsheet_reader.read_tldr())
	return jsonify(msg_to_send)

def whois(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405

	verify_web_hook(request.form)
	msg_to_send = format_slack_message(gsheet_reader.read_tldr(request.form['text']))
	return jsonify(msg_to_send)