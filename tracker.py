# Imports
from bs4 import BeautifulSoup
import requests
import json
from lxml import html
import sys
from datetime import date
import os
from send import SendEmail

# Constant URL that we scrape
url = 'https://spu.edu/administration/health-services/covid-19-cases'

# Setup for lxml
page = requests.get(url)
tree = html.fromstring(page.content)

# Use these lists to store data
cases = []
dates = []

# This is the path to the div that stores the updated data
path_to_cases = '//*[@id="pageBody"]/div/p/text()'
path_to_dates = '//*[@id="pageBody"]/div/p/strong/text()'

# Get cases and add to cases list
for element in tree.xpath(path_to_cases):
    cases.append(element)

# Get dates and append to dates list
for element in tree.xpath(path_to_dates):
    dates.append(element)

# Check to make sure length is the same for both lists
if len(cases) != len(dates):
    sys.exit('ERROR. Cases list length: {}. Dates list length: {}'.format(
        len(cases), len(dates)))

# Store the number of cases
current_num_cases = len(cases)
print('current number of cases: {}'.format(current_num_cases))

if IsNewCase(current_num_cases):
    SendEmail()

# Cases Output
for x in range(0, current_num_cases):
    print('{}: {}'.format(dates[x], cases[x]))

# Get the date from SPU website
spu_last_updated = str(tree.xpath('//*[@id="pageBody"]/div/p[6]/em/text()'))
date_spu_last_updated = spu_last_updated.strip("['Last updated: ']",)

# Format today's date
today = str(date.today()).split('-')
today = '{}/{}/{}'.format(today[1], today[2], today[0])

print('Last Update From SPU: ', date_spu_last_updated)
print('Last Update From Tutorly: ', today)
