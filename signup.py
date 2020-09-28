import os
from slack import WebClient

client = WebClient(token=os.environ["SLACK_API_TOKEN"])
response = client.conversations_list()
conversations = response["channels"]