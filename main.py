import json
from flask import jsonify

with open('config.json', 'r') as jsonfile:
	jsondata = jsonfile.read()
config = json.loads(jsondata)


def verify_web_hook(form):
	if not form or form.get('token') != config['SLACK_TOKEN']:
		raise ValueError('Invalid request/credentials.')

def format_slack_message(query, response):
	message = {
	'response_type': 'in_channel',
	'text': 'Query: {}'.format(query),
	'attachments': []
	}

	attachment = {}
	attachment['color'] = '#3367d6'
	attachment['title'] = response

	message['attachments'].append(attachment)

	return message

def say_hello(query):
	result = 'Hello, World!'
	return format_slack_message(query, result)


def hello_world(request):
	if request.method != 'POST':
		return 'Only POST requests are accepted', 405
	
	verify_web_hook(request.form)
	msg_to_send = say_hello(request.form['text'])
	return jsonify(msg_to_send)