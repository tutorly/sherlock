# Imports
import requests
import json
from lxml import html
import sys
from datetime import date
import os
import time
import smtplib
import os


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
        print('Starting up the boosters')
        self.doScrape()
        self.checkForNewEmails()

    def getStoredCases(self):
        """
        This function will read cases.txt and return the count.
        """
        f = open('cases.txt')
        count = f.read()
        f.close()
        return count

    def sendEmail(self):
        """
        Sends emails to specified list of recipients.
        """
        # This is an env var that stores the tutorly gmail temp password. Your local machine must be configured to have this.
        password = os.getenv('tutorly_gmail_temp_password')

        # ----------------- E-Mail List ----------------------
        toAddress = ['sorenrood@gmail.com', 'stevenkotansky@outlook.com']
        # -----------------------------------------------------

        conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
        conn.ehlo()  # call this to start the connection
        # starts tls encryption. When we send our password it will be encrypted.
        conn.starttls()
        conn.login('tutorlyeducation@gmail.com', password)
        conn.sendmail('tutorlyeducation@gmail.com', toAddress,
                      'Subject: New COVID-19 case confirmed at SPU \n\nSPU COVID-19 Tracker V1.0')
        conn.quit()
        print('Sent notificaton e-mails for the following recipients:\n')
        for i in range(len(toAddress)):
            print(toAddress[i])
        print('')

    def setNumCases(self, cases):
        """
        This function will write the last scraped value to the txt file.
        """
        f = open('cases.txt', 'w')
        f.write(str(cases))
        f.close()

    def doScrape(self):
        # Setup for lxml
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        # This is the path to the div that stores the updated data
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
        # Store the number of cases
        current_num_cases = len(self.cases)
        print('current number of cases: {}'.format(current_num_cases))
        # Check if cases has changes
        if int(self.getStoredCases()) != current_num_cases:
            self.sendEmail()
            self.setNumCases(current_num_cases)
        # Cases Output
        for x in range(0, current_num_cases):
            print('{}: {}'.format(self.dates[x], self.cases[x]))
        # Get the date from SPU website
        spu_last_updated = str(tree.xpath(
            '//*[@id="pageBody"]/div/p[6]/em/text()'))
        date_spu_last_updated = spu_last_updated.strip(
            "['Last updated: ']",)  # TODO FIX THIS WARNING
        # Format today's date
        today = str(date.today()).split('-')
        today = '{}/{}/{}'.format(today[1], today[2], today[0])
        # Dates output
        print('Last Update From SPU: ', date_spu_last_updated)
        print('Last Update From Tutorly: ', today)

    def checkForNewEmails(self):
        """
        This functions makes a call to the slack api and checks for newly submitted emails.
        """
        # Slack API request and JSON load
        payload = {'channel': 'G01BE5PUFCM', 'token': os.getenv('SLACK_API_TOKEN')}
        content = requests.get('https://slack.com/api/conversations.history', params=payload).content
        rawjson = json.loads(content)
        messages = rawjson['messages']
        # Loop through each message and handle new emails
        for message in messages:
            if '@' in message['text']:
                # print(message['text'])
                lines = message['text'].split('\n')
                line_with_email = lines[0]
                email = line_with_email.split(' ')
                print(email[3])


    def clearTempLists(self):
        """
        This function will only be used if we decide to loop main.py instead of running from scratch every x minutes.
        It clears all class-member lists.
        """
        self.cases.clear()
        self.dates.clear()
        self.emails.clear()