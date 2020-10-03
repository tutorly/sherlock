import time
from datetime import datetime
import sys

import requests
from lxml import html

class Scraper():
    '''
    This class contains all of the methods relating to scraping SPU's static webpage containing COVID-19 information.
    It is in charge of scraping, cleaning, and pushing to google sheets.
    '''

    def __init__(self):
        # Compile-time constant values
        self._timeout_duration = 60 # The number of seconds to wait before trying to re-establish a connection to the webpage.
        self._spu_covid_url = 'https://spu.edu/administration/health-services/covid-19-cases' # The default website to scrape.
        self._path_to_cases = '//*[@id="pageBody"]/div/p/text()'
        self._path_to_dates = '//*[@id="pageBody"]/div/p/strong/text()'
        self._path_to_last_spu_update = '//*[@id="pageBody"]/div/p[6]/em/text()'
        self.cases = []
        self.dates = []

    def scrape(self):
        '''Scrapes the website, parses the dates and case description out of the HTML, '''

        # Grab the HTML from the SPU covid url.
        htmlData = self.getHTMLFromURL(self._spu_covid_url)
        
        # Parse the date and case description from the html.
        self.parseDataFromHTML(htmlData)

        # Clean the lists of extraneous characters.
        self.cleanLists()

        # Print the timestamps of the most recent data.
        self.printTimestamps(htmlData)

    def getHTMLFromURL(self, url):
        '''Makes a server request for the given url, ensures the response is ok, then returns a formatted html object.'''
        try:
            response = requests.get(url) # Attempt to make a request to the server and wait for the response.
            if response.status_code != 200: # If the response is not 200 (OK), wait and try again (recursively).
                print(f'Could not connect to {url}. Retrying in {self._timeout_duration} seconds...')
                time.sleep(self._timeout_duration)
                self._sendAdminEmail('Help! The SPU page is down!') # TODO This will send as many emails as calls of this method
                self.getHTMLFromURL(url) # TODO Make sure we don't overflow the call stack (TIMEOUT_DURATION must be reasonable)
            else:
                return html.fromstring(response.content) # Pull the content out of the response and format it as an HTML object
        except ConnectionError:
            self._sendAdminEmail('Sherlock died due to a connection error. Send help.')
            pass

    def parseDataFromHTML(self, htmlData):
        '''To be written.'''
        # Get dates and append to dates list.
        for element in htmlData.xpath(self._path_to_dates):
            print(element)
            self.dates.append(element)

        # Get cases and appends to cases list.
        for element in htmlData.xpath(self._path_to_cases):
            print(element)
            self.cases.append(element)

    def cleanLists(self):
        '''The goal of this function is to make all of the data uniform.'''
        # Check to make sure length is the same for both lists
        if len(self.cases) != len(self.dates):
            msg = f'ERROR. Cases list length: {len(self.cases)}. Dates list length: {len(self.dates)}'
            self._sendAdminEmail(msg)

        # Look for all \xa0 characters and remove them
        for i in range(0, len(self.cases) - 1):
            self.cases[i] = self.cases[i].replace(u'\xa0', ' ').strip()
            self.dates[i] = self.dates[i].replace(u'\xa0', ' ').strip()

    def printTimestamps(self, htmlData):
        '''Prints a formatted timestamp of the last SPU update and the last Tutorly update.'''
        # Get the date from SPU website
        raw_spu_date = str(htmlData.xpath(self._path_to_last_spu_update))
        raw_spu_date = "Last updated: 10/2/20"
        last_spu_update = raw_spu_date.strip(str('Last updated: '))
        
        # Format of today's date: "Thu Oct 1 @ 10:57:01 PM" for more information about strftime, see https://strftime.org
        today = datetime.today().strftime("%m/%d/%y")
        print('Last Update From SPU: ', last_spu_update)
        print('Last Update From Tutorly: ', today)
    
    def _sendAdminEmail(self, msg):
        '''Sends an email to the admin with the given message (Unimplemented).'''
        print(msg)
        pass
       