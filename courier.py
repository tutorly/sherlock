import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import gspread
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np


class Courier():
    '''
    This class contains all of the functions relating to informing people about new cases.
        Courier (v1 - Email) is responsible for deciding which email list to pick and sending beautiful emails to everyone on that list.
        Courier (v2 - Twitter) is responsible for submitting a new post to the Tutorly COVID account using the Twitter API.
    '''

    def postToTwitter(self):
        '''Posts the most recent SPU case to a tutorly twitter account.'''
        pass
    
    @staticmethod
    def sendEmailsToEveryoneInMailingList(msg):
        '''Send emails using smpt library to every email in the self.emails list.'''
        mailing_list = Courier._getUpdatedMailingListFromGoogleSheets()
        sender_name = 'The Tutorly Team'
        subject = 'New COVID-19 case confirmed at SPU'
        person = Courier._getMostRecentCovidCaseDescription()
        time = datetime.today().strftime('%A, %B %Y') 
        body = f'{person} tested positive for COVID-19. More info: https://covid.tutorly.app\nSent at {time}'
        Courier._sendEmails(sender_name, mailing_list, subject, body)

    @staticmethod
    def sendEmailsToAdminOnly(msg):
        '''Sends an email to the admins with the given message.'''
        sender_name = 'Sherlock Admin'
        admin_email_list = ['soren@tutorly.app', 'justin@tutorly.app', 'steven@tutorly.app']
        subject = 'Connection Error'
        Courier._sendEmails(sender_name, admin_email_list, subject, msg)

    @staticmethod
    def _getGoogleSheet(sheet_tab_name):
        '''Returns a reference to the Google Sheet object with the given tab name.'''

        # Connect to the Google Sheets API and return the given sheet tab.
        scope = [
            "https://spreadsheets.google.com/feeds",
            'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("SPU COVID-19 Tracking")
        return sheet.worksheet(sheet_tab_name)
    
    @staticmethod
    def _getUpdatedMailingListFromGoogleSheets():
        '''
        Updates the mailing list from google sheets.

        The creds.json is used to store Google service account credentials hidden by default. You can find this file
        by searching 'creds.json' in the #development slack channel.
        '''

        # Read google sheet into a dataframe, drop blank rows, and remove duplicates.
        sherlock = Courier._getGoogleSheet('emails')
        df = pd.DataFrame(sherlock.get_all_records())
        df = df.replace('', np.nan)
        df = df.dropna()
        emails_df = df['emails']
        emails_df = emails_df.drop_duplicates()

        # Loop through the emails dataframe and append them to a list to be returned.
        mailing_list = []
        for email in emails_df:
            mailing_list.append(email)
        return mailing_list

    @staticmethod
    def _getMostRecentCovidCaseDescription():
        ''' Grabs the most recent case description from the Google Sheet'''

        # Grab the google sheet
        sherlock = Courier._getGoogleSheet('caseLog')
        df = pd.DataFrame(sherlock.get_all_records())
        case_description = df['case'][0]
        return case_description

    @staticmethod
    def _sendEmails(msg_from, to_addrs, subject, body):
        '''
        Send an email using the gmail smtp client with the given subject, sender name, and message body.
        
        Parameters:
            msg_from -- Who the email should be sent from.
            to_addrs -- The recipients of the email(s) you are sending.
            subject -- The subject of the email(s) that you want to send.
            body -- The body of the message that you want to send (formatted as plain-text for now).
        '''

        # Get username and password for the email account, pull password from local environment variables
        username = 'covid@tutorly.app'
        password = os.getenv('covid_tutorly_password')
        
        # Construct the message body with the given attributes.
        message = MIMEMultipart()
        message['From'] = msg_from
        message['Subject'] = subject
        message_body = MIMEText(body, 'plain')
        message.attach(message_body)

        # Establish a secure connection to the gmail smtp server and send the message.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, to_addrs, message.as_string())
        server.quit()

        # [OPTIONAL] Log the emails that were sent to the console for reference.
        print(f'Sent {len(to_addrs)} emails to:\n')
        print(*to_addrs, sep = '\n') # Prints each email address from the list on its own line.
