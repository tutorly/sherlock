# Imports
import requests
import json
from lxml import html
import sys
from datetime import date
import os
import time
import smtplib
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import numpy as np

def writeEmailsToGoogleSheets(self):
    """
    Write this later. This is for data visualiation.
    """
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("SPU COVID-19 Tracking")
    caseLog = sheet.worksheet('caseLog')

    # Write emails to spreadsheet
    for i in len(self.emails):
        caseLog.update_cell(i, 1, self.emails[i - 1])

    # Write names to spreadsheet
    for i in len(self.dates):
        caseLog.update_cell(i, 2, self.dates[i - 1])


