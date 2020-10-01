import json
import os
import smtplib
import sys
import time
from datetime import date
from pprint import pprint

import gspread
import numpy as np
import pandas as pd
import requests
from lxml import html
from oauth2client.service_account import ServiceAccountCredentials


def writeDataToGoogleSheets(self):
    """
    Write this later. This is for data visualiation.
    """
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("SPU COVID-19 Tracking")
    caseLog = sheet.worksheet('caseLog')

    # Write emails to spreadsheet
    for i in len(self.dates):
        caseLog.update_cell(i, 1, self.dates[i - 1])



