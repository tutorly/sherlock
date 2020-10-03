import time
from datetime import datetime

import requests
from lxml import html

class Scraper():
    '''This class contains all of the methods relating to scraping SPU's static webpage containing COVID-19 information.
    It is in charge of scraping, cleaning, and pushing to google sheets.'''

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
        self.parseDateFromHTML(htmlData)
        self.parseCasesFromHTML(htmlData)

        # Clean the lists of extraneous characters.
        self.cleanLists()

        # Check if there is a new case.
        self.isNewCase()

        # Print the timestamps of the most recent data.
        self.printTimestamps(htmlData)

    def getHTMLFromURL(self, url):
        '''Makes a server request for the given url, ensures the response is ok, then returns a formatted html object.'''
        try:
            response = requests.get(url) # Attempt to make a request to the server and wait for the response.
            if (response.status_code != 200): # If the response is not 200 (OK), wait and try again (recursively).
                print(f'Could not connect to {url}. Retrying in {self._timeout_duration} seconds...')
                time.sleep(self._timeout_duration)
                self.sendAdminEmail('Help! The SPU page is down!') # TODO This will send as many emails as calls of this method
                self.getHTMLFromURL(url) # TODO Make sure we don't overflow the call stack (TIMEOUT_DURATION must be reasonable)
            else:
                return html.fromstring(response.content) # Pull the content out of the response and format it as an HTML object
        except ConnectionError:
            self.sendAdminEmail('Sherlock died due to a connection error. Send help.')
            pass

    def parseDateFromHTML(self, htmlData):
        '''Parses the dates from the given HTML and adds them to the DATES array.'''
        # Get dates and append to dates list
        for element in htmlData.xpath(self._path_to_dates):
            self.dates.append(element)

    def parseCasesFromHTML(self, htmlData):
        '''Parses the cases from the given HTML and adds them to the CASES array.'''
        # Get cases and add to cases list
        for element in htmlData.xpath(self._path_to_cases):
            self.cases.append(element)

    def cleanLists(self):
        '''The goal of this function is to make all of the data uniform.'''
        # Check to make sure length is the same for both lists
        if len(self.cases) != len(self.dates):
            msg = f'ERROR. Cases list length: {len(self.cases)}. Dates list length: {len(self.dates)}'
            self.sendAdminEmail(msg)

        # Look for all \xa0 characters and remove them
        for i in range(0, len(self.cases) - 1):
            self.cases[i] = self.cases[i].replace(u'\xa0', ' ').strip()
            self.dates[i] = self.dates[i].replace(u'\xa0', ' ').strip()

    def isNewCase(self):
        """
        This function checks if there is a new case by looking at the length of the self.cases list length and
        cross referencing it with the cases.txt number (USE DATABASE MODULE).
        """

        ####################################
        # TALK TO JUSTIN ABOUT THIS METHOD #
        ####################################

        # current_num_cases = len(self.CASES)
        # print(f'Found {current_num_cases} cases on last scrape.')

        # # Check if cases has changes
        # if int(self.getStoredCases()) != current_num_cases:
        #     newest_case = str('{}: {}'.format(self.dates[0], self.cases[0]))
        #     self.sendEmails(newest_case) # TODO Change this into notify function so that I can do emails/twitter/other things
        #     self.setNumCases(current_num_cases)
            
        # # Print cases
        # for x in range(0, current_num_cases):
        #     print('{}: {}'.format(self.dates[x], self.cases[x]))

    def printTimestamps(self, htmlData):
        '''Prints a formatted timestamp of the last SPU update and the last Tutorly update.'''
        # Get the date from SPU website
        raw_spu_date = str(htmlData.xpath(self._path_to_last_spu_update)[0])
        raw_spu_date = "Last updated: 10/2/20"
        last_spu_update = raw_spu_date.strip(['Last updated: '])
        
        # Format of today's date: "Thu Oct 1 @ 10:57:01 PM" for more information about strftime, see https://strftime.org
        today = datetime.today().strftime('%a %b %-d @ %-I:%M:%S %p')
        print('Last Update From SPU: ', last_spu_update)
        print('Last Update From Tutorly: ', today)
    
    def sendAdminEmail(self, msg):
        '''Sends an email to the admin with the given message (Unimplemented).'''
        print(msg)
        pass
       