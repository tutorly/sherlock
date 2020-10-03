import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

class Validator():
    '''This class contains all of the methods to determine if the scraper has picked up a new case or not.'''

    def __init__(self):
        '''To be written.'''
        self.cases = []
        self.dates = []

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

    def getDataFromGoogleSheets(self):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        workbook = client.open("SPU COVID-19 Tracking")
        sheet = workbook.worksheet('caseLog')

        # Read in all records from caseLog tab in gsheets. Separate dates and cases columns. 
        df = pd.DataFrame(sheet.get_all_records())
        dates = df['date']
        cases = df['case']

        # Drop NA values for cases and dates columns
        dates = dates.replace('', np.nan)
        dates = dates.dropna()
        cases = cases.replace('', np.nan)
        cases = cases.dropna()
        
        # Send dates and cases to self.cases and self.dates
        for date in dates:
            self.dates.append(date)
        for case in cases:
            self.cases.append(case)
        

