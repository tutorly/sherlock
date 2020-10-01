import datetime
import json
import os
import smtplib
import sys
import time
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint

import gspread
import numpy as np
import pandas as pd
import requests
from lxml import html
from oauth2client.service_account import ServiceAccountCredentials


class Session():
    """
    This class does everything from web scraping to sending emails. It's a beast.
    """
    def __init__(self):
        """
        Initializes with the URL, a list of temporary cases per scrape, a list of dates per scrape, and an integer from cases.txt.
        """
        self.url = 'https://spu.edu/administration/health-services/covid-19-cases'
        self.cases = []
        self.dates = []
        self.emails = []

    def run(self):
        """
        Method that drives the program.
        """
        count = 0
        while(1):
            print('----------------------------- loop: {} timestamp: {}'.format(count, datetime.datetime.now()))
            self.doScrape()
            self.writeListsToGoogleSheet()
            self.clearTempLists()
            print('-----------------------------')
            count = count + 1
            time.sleep(60)

    def getStoredCases(self):
        """
        This function will read cases.txt and return the count.
        """
        f = open('cases.txt')
        count = f.read()
        f.close()
        return count

    def sendEmails(self, body):
        """
        Send emails using smpt library to every email in the self.emails list.
        """
        # Pull an updated list of emails from Google Sheets and update self.emails
        self.getEmails()

        # Initialize a connection to the Gmail SMTP server on port 587.
        server = smtplib.SMTP('smtp.gmail.com', 587)        

        # Use TLS encryption and log into the SMTP server with user credentials.
        username = 'covid@tutorly.app'
        password = os.getenv('covid_tutorly_password') # pull password from local environment variables
        server.starttls() # Enable TLS encryption so our password will be encrypted.
        server.login(username, password)

        # Send an email to each of the addresses in the email list with the given message.
        message = MIMEMultipart()
        message['From'] = 'The Tutorly Team'
        message['Subject'] = 'New COVID-19 case confirmed at SPU'
        plainTextBody = MIMEText(body, 'plain')
        message.attach(plainTextBody)
        server.sendmail(username, self.emails, message.as_string())
        server.quit()

        # Log the emails that were sent to the console for reference.
        emailList = self.emails
        print('Sent {} emails to:\n'.format(len(emailList)))
        print(*emailList, sep = '\n') # Prints each email address from the list on its own line.

    def setNumCases(self, cases):
        """
        This function will write the last scraped value to cases.txt.
        """
        f = open('cases.txt', 'w')
        f.write(str(cases))
        f.close()

    def doScrape(self):
        """
        This function scrapes the url contained in self.url and looks for a specific html tag's xpath that contains new SPU covid cases. It itterates over the elements within and appends
        the values to self.cases and self.dates.
        """
        website_up = False
        while(website_up == False):
            # This logic exists so that the bot does not die if the website is down.
            try:
                page = requests.get(self.url)
                website_up = True
            except:
                print('Could not connect to {}... Retrying in 5 seconds.'.format(self.url))
                time.sleep(5)
        
        # This is the path to the div that stores the updated data (lxml lib)
        tree = html.fromstring(page.content)
        path_to_cases = '//*[@id="pageBody"]/div/p/text()'
        path_to_dates = '//*[@id="pageBody"]/div/p/strong/text()'

        # Get cases and add to cases list
        for element in tree.xpath(path_to_cases):
            element = element.replace(u'\xa0', ' ')
            self.cases.append(element)

        # Get dates and append to dates list
        for element in tree.xpath(path_to_dates):
            element = element.replace(u'\xa0', ' ')
            self.dates.append(element)

        # Clean up the lists
        self.cleanLists()

        # Check to make sure length is the same for both lists
        if len(self.cases) != len(self.dates):
            sys.exit('ERROR. Cases list length: {}. Dates list length: {}'.format(
                len(self.cases), len(self.dates)))

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
       

    def getEmails(self):
        """
        Get emails from google sheets api and adds contents to self.emails list.
        """
        # Connect with our google sheet. The creds.json is hidden by default. (You can find this file by searching 'creds.json' in development slack channel.)
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("SPU COVID-19 Tracking")
        sherlock = sheet.worksheet('emails')

        # Read google sheet into a dataframe, drop blank rows, appends all emails to self.emails.
        df = pd.DataFrame(sherlock.get_all_records())
        df = df.replace('', np.nan)
        df = df.dropna()
        for email in df['emails']:
            self.emails.append(email)

    def clearTempLists(self):
        """
        This function clears self.cases, self.dates, and self.emails.
        """
        self.cases.clear()
        self.dates.clear()
        self.emails.clear()

    def writeListsToGoogleSheet(self):
        """
        This function writes the contents of self.dates and self.cases to SPU COVID-19 Tracking Google Sheet. This sheet is available on the Tutorlyeducation gmail account.
        """
        # self.doScrape()
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        workbook = client.open("SPU COVID-19 Tracking")
        sheet = workbook.worksheet('caseLog')
        
        # Write self.dates to gsheets
        count = 2 # count is 2 because we start populating spreadsheet at row 2 (1 is headers)
        for date in self.dates:
            sheet.update_cell(count, 1, date)
            count = count + 1
        
        # Write self.cases to gsheets
        count = 2
        for case in self.cases:
            sheet.update_cell(count, 2, case)
            count = count + 1

        print('Data updated in google sheets')

    def postToTwitter(self):
        """
        Posts the most recent SPU case to a tutorly twitter account.
        """
        pass

    def cleanLists(self):
        """
        The goal of this function is to make all of the data uniform.
        """
        # Fix cases list
        for case in self.cases:
            case = case.replace(u'\xa0', u'') # TODO THESE DONT WORK RIGHT NOW

        # Fix dates list
        for date in self.dates:
            date = date.replace(u'\xa0', u'')

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
        