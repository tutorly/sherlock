import datetime
import json
import os
import smtplib
import sys
import time
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
import numpy as np
import pandas as pd
import requests
from lxml import html
from oauth2client.service_account import ServiceAccountCredentials

from scraper import Scraper
from validator import Validator
from courier import Courier

class Session():
    '''To be written.'''
    def __init__(self):
        '''To be written.'''
        self.scraper = Scraper()
        self.validator = Validator()
        self.courier = Courier()

    def run(self):
        '''This is the method that drives the entire program.'''
        self.scraper.scrape()

    def clearTempLists(self):
        '''Clears lists from scraper, validator, and courier.'''
        self.scraper.emptyLists()
        self.validator.emptyLists()