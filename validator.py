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
        self.num_cases_last_scraped = 0 
        self.num_cases_recorded = 0

    def checkForNewCase(self):
        '''
        To be written.
        '''
        self.getLastScrapeFromGoogleSheets()
        self.countScrapedCases()
        self.getRecordedCaseNum()

        # If the last scrape is not equal to the previous number of cases.
        if self.num_cases_last_scraped != self.num_cases_recorded:
            # new case

    def getLastScrapeFromGoogleSheets(self):
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
        
    def countScrapedCases(self):
        '''To be written.'''
        for case in self.cases:
            self.num_cases_last_scraped = self.num_cases_last_scraped + int(case.split(' ')[0])
    
    def incrementTotalCasesCount(self):
        '''Only called when self.num_cases_last_scraped is greater than the number of the last recorded max count.'''
        # Connect to google sheet
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        workbook = client.open("SPU COVID-19 Tracking")
        sheet = workbook.worksheet('numCases')

        # Update cell
        sheet.update_cell(1, 1, self.num_cases_last_scraped)
    
    def getRecordedCaseNum(self):
        '''
        Returns the number of cases as as integer (according to google sheets). 
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

    def updateNewCaseCount(self):
        pass
        
