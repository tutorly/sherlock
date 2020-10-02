import time
from datetime import datetime

import requests
from lxml import html

class WebScraper():
    '''Exposes a simple API used to scrape a static webpage.'''

    # Compile-time constant values (I put them here for easy access, not sure if this is 'pythonic' or not).
    TIMEOUT_DURATION = 60 # The number of seconds to wait before trying to re-establish a connection to the webpage.
    SPU_COVID_URL = 'https://spu.edu/administration/health-services/covid-19-cases' # The default website to scrape.
    PATH_TO_CASES = '//*[@id="pageBody"]/div/p/text()'
    PATH_TO_DATES = '//*[@id="pageBody"]/div/p/strong/text()'
    PATH_TO_SPU_DATE = '//*[@id="pageBody"]/div/p[6]/em/text()'
    CASES = []
    DATES = []

    def scrape(self):
        # Grab the HTML from the SPU covid url.
        htmlData = self.getHTMLFromURL(self.SPU_COVID_URL)

        # Parse the date and case description from the html.
        self.parseDateFromHTML(htmlData)
        self.parseCasesFromHTML(htmlData)

        # Clean the lists of extraneous characters.
        self.cleanLists

        # Check if there is a new case.
        self.isNewCase()


    def cleanLists(self):
        '''The goal of this function is to make all of the data uniform.'''
        # Check to make sure length is the same for both lists
        if len(self.CASES) != len(self.DATES):
            msg = f'ERROR. Cases list length: {len(self.CASES)}. Dates list length: {len(self.DATES)}'
            self.sendAdminEmail(msg)

        # Look for all \xa0 characters and remove them
        for i in range(0, len(self.CASES) - 1):
            self.CASES[i] = self.CASES[i].replace(u'\xa0', ' ').strip()
            self.DATES[i] = self.DATES[i].replace(u'\xa0', ' ').strip()

    def isNewCase(self):
        """
        This function checks if there is a new case by looking at the length of the self.cases list length and
        cross referencing it with the cases.txt number (USE DATABASE MODULE).
        """
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

    def getHTMLFromURL(self, url):
        '''Makes a server request for the given url, ensures the response is ok, then returns a formatted html object.'''
        try:
            response = requests.get(url) # Attempt to make a request to the server and wait for the response.
            if (response.status_code != 200): # If the response is not 200 (ok), wait and try again (recursively).
                print(f'Could not connect to {url}. Retrying in {self.TIMEOUT_DURATION} seconds...')
                time.sleep(self.TIMEOUT_DURATION)
                # TODO sendAdminEmail() # Notify admin that the website is down. (This would send as many emails as iterations of this method)
                self.getHTMLFromURL(url) # TODO Make sure we don't overflow the call stack (TIMEOUT_DURATION must be reasonable)
            else:
                return html.fromstring(response.content) # Pull the content out of the response and format it as an HTML object
        except ConnectionError:
            # TODO sendAdminEmail() # In the event of a network problem, requests will raise a ConnectionError exception.
            pass

    def sendAdminEmail(self, msg):
        '''Sends an email to the admin with the given message (Unimplemented).'''
        print(msg)
        pass

    def parseDateFromHTML(self, htmlData):
        '''Parses the dates from the given HTML and adds them to the DATES array.'''
        # Get dates and append to dates list
        for element in htmlData.xpath(self.PATH_TO_DATES):
            self.DATES.append(element)

    def parseCasesFromHTML(self, htmlData):
        '''Parses the cases from the given HTML and adds them to the CASES array.'''
        # Get cases and add to cases list
        for element in htmlData.xpath(self.PATH_TO_CASES):
            self.CASES.append(element)

    def printTimestamps(self, htmlData):
        # Get the date from SPU website
        raw_spu_date = str(htmlData.xpath(self.PATH_TO_SPU_DATE)[0])
        raw_spu_date = "Last updated: 10/2/20"
        last_spu_update = raw_spu_date.strip(['Last updated: '])
        
        # Format of today's date: "Thu Oct 1 @ 10:57:01 PM" for more information about strftime, see https://strftime.org
        today = datetime.today().strftime('%a %b %-d @ %-I:%M:%S %p')
        print('Last Update From SPU: ', last_spu_update)
        print('Last Update From Tutorly: ', today)
       