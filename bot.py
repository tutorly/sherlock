import datetime
import time

from scraper import Scraper
from validator import Validator
from courier import Courier

class Bot():
    '''This bot contains a scraper, a validator, and a courier. It is epic.'''
    def __init__(self):
        '''Initializes bot class.'''
        self.scraper = Scraper()
        self.validator = Validator()
        self.courier = Courier()
        self.loopInterval = 60 # In seconds

    def run(self):
        '''This is the method that drives the entire program.'''
        input('do you want to run in testing mode or production mode? t/p')
        while(1):
            print('-------------')
            self.scraper.scrape()
            if self.validator.checkForNewCase():
                print('NEW CASE FOUND')
                Courier.sendEmailsToAdminOnly('New case message')
            self.cleanUp()
            print('-------------')
            time.sleep(self.loopInterval)

    def cleanUp(self):
        '''CleanUp crew for scraper, validator, and courier.'''
        self.scraper.cleanUp()
        self.validator.cleanUp()