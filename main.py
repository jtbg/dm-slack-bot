import json
from flask import jsonify

with open('config.json', 'r') as jsonfile:
    jsondata = jsonfile.read()
config = json.loads(jsondata)


def verify_web_hook(form):
    if not form or form.get('token') != config['SLACK_TOKEN']:
        raise ValueError('Invalid request/credentials.')