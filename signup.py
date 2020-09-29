import os
import requests
import json

payload = {'channel': 'G01BE5PUFCM', 'token': os.getenv('SLACK_API_TOKEN')}

resp = requests.get('https://slack.com/api/conversations.history', params=payload)
print(resp.content)