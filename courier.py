import datetime
import json
import os
import smtplib
import sys
import time
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
import numpy as np
import pandas as pd
import requests
from lxml import html
from oauth2client.service_account import ServiceAccountCredentials

# from scraper import Scraper
from validator import Validator

class Courier():
    '''
    This class contains all of the functions relating to informing people about new cases.
    Courier (v1 - Email) is responsible for deciding which email list to pick and sending beautiful emails to everyone on that list.
    Courier (v2 - Twitter) is responsible for submitting a new post to the Tutorly COVID account using the Twitter API.
    '''

    def __init__(self):
        self.email_list = []

    def updateEmailList(self):
        """
        Select and grab the correct email list from the Google Sheets API and adds contents to the local email list.
        The creds.json is used to store Google service account credentials hidden by default. You can find this file
        by searching 'creds.json' in development slack channel.)
        """

        # Connect with our Google Sheet.
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("SPU COVID-19 Tracking")
        sherlock = sheet.worksheet('emails') # for tests use 'testingEnvironment'

        # Read google sheet into a dataframe, drop blank rows, appends all emails to self.emails.
        df = pd.DataFrame(sherlock.get_all_records())
        df = df.replace('', np.nan)
        df = df.dropna()
        for email in df['emails']:
            self.email_list.append(email)

    def sendEmails(self, body):
        '''Send emails using smpt library to every email in the self.emails list.'''

        # Get username and password for the 
        username = 'covid@tutorly.app'
        password = os.getenv('covid_tutorly_password') # pull password from local environment variables

        server = smtplib.SMTP('smtp.gmail.com', 587)        
        server.starttls() # Enable TLS encryption so our password will be encrypted.
        server.login(username, password)

        # Send an email to each of the addresses in the email list with the given message.
        message = MIMEMultipart()
        message['From'] = 'The Tutorly Team'
        message['Subject'] = 'New COVID-19 case confirmed at SPU'
        final_body = 'New case from SPU website. {}'.format(body)
        plainTextBody = MIMEText(final_body, 'plain')
        message.attach(plainTextBody)
        # server.sendmail(username, self.emails, message.as_string()) # Commented out for safety
        server.quit()

        # Log the emails that were sent to the console for reference.
        emailList = self.email_list
        print('Sent {} emails to:\n'.format(len(emailList)))
        print(*emailList, sep = '\n') # Prints each email address from the list on its own line.

    def sendEmails(self, body):
        '''Send emails using smpt library to every email in the self.emails list.'''

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
        final_body = 'New case from SPU website. {}'.format(body)
        plainTextBody = MIMEText(final_body, 'plain')
        message.attach(plainTextBody)
        # server.sendmail(username, self.emails, message.as_string()) # Commented out for safety
        server.quit()

        # Log the emails that were sent to the console for reference.
        emailList = self.email_list
        print('Sent {} emails to:\n'.format(len(emailList)))
        print(*emailList, sep = '\n') # Prints each email address from the list on its own line.

    @staticmethod
    def sendAdminEmail(msg):
        '''Sends an email to the admins with the given message.'''

        admin_email_list = ['soren@tutorly.app', 'justin@tutorly.app', 'steven@tutorly.app']

        # Initialize a connection to the Gmail SMTP server on port 587.
        server = smtplib.SMTP('smtp.gmail.com', 587)        

        # Use TLS encryption and log into the SMTP server with user credentials.
        username = 'covid@tutorly.app'
        password = os.getenv('covid_tutorly_password') # pull password from local environment variables
        server.starttls() # Enable TLS encryption so our password will be encrypted.
        server.login(username, password)

        # Send an email to each of the addresses in the email list with the given message.
        message = MIMEMultipart()
        message['From'] = 'Sherlock Admin'
        message['Subject'] = 'Connection Error'
        # time = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        final_body = f'{time}\n\n{msg}' 
        plainTextBody = MIMEText(final_body, 'plain')
        message.attach(plainTextBody)
        server.sendmail(username, admin_email_list, message.as_string()) # Commented out for safety
        server.quit()

        # Log the emails that were sent to the console for reference.
        print(f'Sent {len(admin_email_list)} emails to:\n')
        print(*admin_email_list, sep = '\n') # Prints each email address from the list on its own line.

    def postToTwitter(self):
        '''Posts the most recent SPU case to a tutorly twitter account.'''
        pass

#### PRIVATE HELPER FUNCTIONS ####