import os
import requests
import json

# Slack API request and JSON load
payload = {'channel': 'G01BE5PUFCM', 'token': os.getenv('SLACK_API_TOKEN')}
content = requests.get('https://slack.com/api/conversations.history', params=payload).content
rawjson = json.loads(content)
messages = rawjson['messages']

# Loop through each message and handle new emails
for message in messages:
    if '@' in message['text']:
        print(element['text'])
