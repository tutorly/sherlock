import requests

class WebScraper():
    '''Exposes a simple API used to scrape a static webpage.'''

    SPU_COVID_URL = 'https://spu.edu/administration/health-services/covid-19-cases'

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

    def getHTML

    def doScrape(self):
        """
        This function scrapes the url contained in self.url and looks for a specific html tag's xpath
        that contains new SPU covid cases. It itterates over the elements within and appends
        the values to self.cases and self.dates.
        """

        response = requests.get(self.SPU_COVID_URL)



        # website_up = False
        # while(website_up == False):
        #     # This logic exists so that the bot does not die if the website is down.
        #     try:
        #         page = requests.get(self.url)
        #         website_up = True
        #     except:
        #         print('Could not connect to {}... Retrying in 5 seconds.'.format(self.url))
        #         # sendAdminEmail() TODO
        #         time.sleep(5)
        
        # This is the path to the div that stores the updated data (lxml lib)
        tree = html.fromstring(page.content)
        path_to_cases = '//*[@id="pageBody"]/div/p/text()'
        path_to_dates = '//*[@id="pageBody"]/div/p/strong/text()'

        # Get cases and add to cases list
        for element in tree.xpath(path_to_cases):
            self.cases.append(element)

        # Get dates and append to dates list
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
        last_spu_update = raw_spu_date.strip("['Last updated: ']")  # TODO FIX THIS WARNING
        
        # Format today's date
        today = str(date.today()).split('-')
        today = '{}/{}/{}'.format(today[1], today[2], today[0])
        print('Last Update From SPU: ', last_spu_update)
        print('Last Update From Tutorly: ', today)
       