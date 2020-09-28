# Imports
from bs4 import BeautifulSoup
import requests
import json
from lxml import html
import sys
from datetime import date

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
number_of_cases = len(cases)

# Output
for x in range(0, number_of_cases):
    print('{}: {}'.format(dates[x], cases[x]))

# Date output
spu_last_updated = str(tree.xpath('//*[@id="pageBody"]/div/p[6]/em/text()'))
date_spu_last_updated = spu_last_updated.strip("['Last updated: ']",)

print('Last Update From SPU: ', date_spu_last_updated)

today = str(date.today())

today = today.split('-')

today = '{}/{}/{}'.format(today[1], today[2], today[0])

print('Last Update From Tutorly: ', today)
