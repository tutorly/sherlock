# File written by Soren on 9/30/2020

# Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd

# Connect with our google sheet. The creds.json is hidden by default. Soren has access to it. 
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("SPU COVID-19 Tracking")
sherlock = sheet.worksheet('Sheet4')

# Use pandas here to work with large data
df = pd.DataFrame(sherlock.get_all_records())
print(df)