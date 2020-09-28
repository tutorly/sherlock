# Imports
from bs4 import BeautifulSoup
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

    def __init__(self):
        """
        Initializes with the URL, a list of temporary cases per scrape, a list of dates per scrape, and an integer from cases.txt.
        """
        self.url = 'https://spu.edu/administration/health-services/covid-19-cases'
        self.cases = []
        self.dates = []

    def run(self):
        print('Starting up the boosters...')
        pass

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
        Sends emails. Remove print statements when we are running this on the raspberry pi.
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
        f.write(cases)
        f.close()
