import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

class Validator():
    '''This class contains all of the methods to determine if the scraper has picked up a new case or not.'''
    def __init__(self):
        '''Initializes the validator.'''
        self.cases = []
        self.dates = []
        self.num_cases_last_scraped = 0
        self.num_cases_recorded = 0 # This stores the value from google sheets. This var and num_cases_last_scraped are compared to check for new cases.

    def checkForNewCase(self):
        '''
        Performs all of the operations to check if there is a new case from the last scrape.
        '''
        self._getLastScrapeFromGoogleSheets()
        self._countScrapedCases()
        self._getNumRecordedCases()

        # If the last scrape is not equal to the previous number of cases.
        if self.num_cases_last_scraped != self.num_cases_recorded:
            self._updateCaseCount()
            return True
        else: return False

    def _getLastScrapeFromGoogleSheets(self):
        '''This method will populate self.cases and self.dates lists with the most recent scrape data.'''
        # Connect to google
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
        
    def _countScrapedCases(self):
        '''This is the method that splits apart the cases so we can account for multiple cases in one day. For example: 2 Students will be able to be recorded as 2 new cases.'''
        for case in self.cases:
            self.num_cases_last_scraped = int(self.num_cases_last_scraped) + int(case.split(' ')[0])
    
    def _getNumRecordedCases(self):
        '''
        Locates the number of cases as as integer and stores in self.num_cases_recorded. (according to google sheets). 
        Located at cell A1 in numCases tab in the 'SPU COVID-19 Tracking' Sheet. 
        '''
        # Connect to google sheet
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        workbook = client.open("SPU COVID-19 Tracking")
        sheet = workbook.worksheet('numCases')

        # Store the value from the gsheet.
        self.num_cases_recorded = int(sheet.acell('A1').value)

    def _updateCaseCount(self):
        '''This method will be called when there is a new (or removed) case from the website.'''
        # Connect to google sheet
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        workbook = client.open("SPU COVID-19 Tracking")
        sheet = workbook.worksheet('numCases')

        # Update the cell!
        sheet.update_cell(1, 1, self.num_cases_last_scraped)
        
