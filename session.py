# Imports
from bs4 import BeautifulSoup
import requests
import json
from lxml import html
import sys
from datetime import date
import os
from helper import sendEmail, getStoredCases


class Session():
    def __init__(self):
        """
        Initializes with the URL, a list of temporary cases per scrape, a list of dates per scrape, and an integer from cases.txt.
        """
        self.url = 'https://spu.edu/administration/health-services/covid-19-cases'
        self.cases = []
        self.dates = []
        self.stored_cases = int(getStoredCases())

    def sayHello(self):
        print('hello world')
