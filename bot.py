import datetime
import time
from enum import Enum

from scraper import Scraper
from validator import Validator
from courier import Courier




class Mode(Enum):
    '''This class is simply an enum to keep track of what mode our bot is currently in. The numbers are entirely arbitrary.'''
    TEST = 0
    PROD = 1


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
        self.modeSelect()
        while(1):
            print('-------------')
            self.scraper.scrape()
            if self.validator.checkForNewCase():
                print('NEW CASE FOUND')
                Courier.sendEmailsToAdminOnly('New case message')
            self.cleanUp()
            print('-------------')
            time.sleep(self.loopInterval)

    def modeSelect(self):
        '''This is the method that helps the user decide what mode to run the bot in.'''
        # List of available modes.
        modes = ['test', 'prod']

        while(1):
            selected_mode = input('Enter "test" for test mode or "prod" for production mode. ')
            if selected_mode in modes:
                print(f'you entered "{selected_mode}". If this is correct, press ENTER. If not, press control + c to cancel.')
                input()
                return
            else: print(f'{selected_mode} is not valid mode.')

    def cleanUp(self):
        '''CleanUp crew for scraper, validator, and courier.'''
        self.scraper.cleanUp()
        self.validator.cleanUp()