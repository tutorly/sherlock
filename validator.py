class Validator():
    '''This class contains all of the methods to determine if the scraper has picked up a new case or not.'''

    def __init__(self):
        '''To be written.'''
        pass

        def isNewCase(self):
            '''
            To be written.
            '''
            # current_num_cases = len(self.cases)
            # print('Found {} cases on last scrape.'.format(current_num_cases))

            # # Check if cases has changes
            # if int(self.getStoredCases()) != current_num_cases:
            #     newest_case = str('{}: {}'.format(self.dates[0], self.cases[0]))
            #     self.sendEmails(newest_case) # TODO Change this into notify function so that I can do emails/twitter/other things
            #     self.setNumCases(current_num_cases)
            return False

        def _getDataFromGoogleSheets(self):
            self