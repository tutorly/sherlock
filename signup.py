import os
import requests
import json

payload = {'channel': 'G01BE5PUFCM', 'token': os.getenv('SLACK_API_TOKEN')}
content = requests.get('https://slack.com/api/conversations.history', params=payload).content
rawjson = json.loads(content)
messages = rawjson['messages']

# Loop through each message
for element in messages:
    print(element['text']) # TODO handle emails here
