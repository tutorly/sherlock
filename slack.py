import slack
import requests

token = ''
endpoint = 'https://slack.com/api/conversations.history?token='
final = '{}{}'.format(endpoint, token)

page = requests.get(final)

print(page.content)
