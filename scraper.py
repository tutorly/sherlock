import time
from datetime import datetime

import requests
from lxml import html

class WebScraper():
    '''Exposes a simple API used to scrape a static webpage.'''

    # Compile-time constant values (I put them here for easy access, not sure if this is 'pythonic' or not).
    SPU_COVID_URL = 'https://spu.edu/administration/health-services/covid-19-cases' # The default website to scrape
    TIMEOUT_DURATION = 60 # The number of seconds to wait before trying to re-establish a connection to the webpage.

    def run(self):
        tree = self.getHTMLFromURL()
        self.parseDateFromHTML(tree)
        self.parseCasesFromHTML(tree)


    def cleanLists(self):
        """
        The goal of this function is to make all of the data uniform. Unfinished logic.
        """
        # Look for all \xa0 characters and remove them
        for i in range(0, len(self.cases) - 1):
            self.cases[i] = self.cases[i].replace(u'\xa0', ' ').strip()
            self.dates[i] = self.dates[i].replace(u'\xa0', ' ').strip()

    def isNewCase(self):
        """
        This function checks if there is a new case by looking at the length of the self.cases list length and
        cross referencing it with the cases.txt number.
        """
        current_num_cases = len(self.cases)
        print('Found {} cases on last scrape.'.format(current_num_cases))

        # Check if cases has changes
        if int(self.getStoredCases()) != current_num_cases:
            newest_case = str('{}: {}'.format(self.dates[0], self.cases[0]))
            self.sendEmails(newest_case) # TODO Change this into notify function so that I can do emails/twitter/other things
            self.setNumCases(current_num_cases)
            
        # Print cases
        for x in range(0, current_num_cases):
            print('{}: {}'.format(self.dates[x], self.cases[x]))

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

    def doScrape(self):
        """
        This function scrapes the url contained in self.url and looks for a specific html tag's xpath
        that contains new SPU covid cases. It iterates over the elements within and appends
        the values to self.cases and self.dates.
        """

        # This is the path to the div that stores the updated data (lxml lib)
        tree = self.getHTMLFromURL(self.SPU_COVID_URL)

        # Get cases and add to cases list
        path_to_cases = '//*[@id="pageBody"]/div/p/text()'
        for element in tree.xpath(path_to_cases):
            self.cases.append(element)

        # Get dates and append to dates list
        path_to_dates = '//*[@id="pageBody"]/div/p/strong/text()'
        for element in tree.xpath(path_to_dates):
            self.dates.append(element)

        # Check to make sure length is the same for both lists
        if len(self.cases) != len(self.dates):
            sys.exit('ERROR. Cases list length: {}. Dates list length: {}'.format(
                len(self.cases), len(self.dates)))
            
        # Clean up the lists
        self.cleanLists()

        # Check for a new case
        self.isNewCase()

         # Get the date from SPU website
        raw_spu_date = str(tree.xpath('//*[@id="pageBody"]/div/p[6]/em/text()'))
        raw_spu_date = "Last updated: 10/2/20"
        last_spu_update = raw_spu_date.strip(['Last updated: '])  # TODO FIX THIS WARNING
        
        # Format of today's date: "Thu Oct 1 @ 10:57:01 PM" for more information about strftime, see https://strftime.org
        today = datetime.today().strftime('%a %b %-d @ %-I:%M:%S %p')
        print('Last Update From SPU: ', last_spu_update)
        print('Last Update From Tutorly: ', today)
       