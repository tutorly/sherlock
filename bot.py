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
        self.currentMode = Mode.TEST # This is set in self.ModeSelect() method in the run method. I have it set to Mode.TEST default incase someone removes self.modeSelect().

    def run(self):
        '''This is the method that drives the entire program.'''
        # Ask the user what mode they want to run the bot in.
        self.currentMode = self.modeSelect()

        # Last output before loop
        print(f'Starting bot in: {self.currentMode}')

        # While loop.
        while(1):
            print('-------------')

            # Let the scraper scrape for new cases.
            self.scraper.scrape()

            # Check if there is a new case from that scrape.
            if self.validator.checkForNewCase():
                print('Sherlock has found a new case.')

                # Logic to decide who gets emails when there is a new case.
                if self.currentMode == Mode.TEST:
                    Courier.sendEmailsToAdminOnly('This is a test.')
                
                if self.currentMode == Mode.PROD:
                    # Courier.sendEmailsToEveryoneInMailingList('New covid-19 case confirmed on campus.')
                    pass

            self.cleanUp()
            print('-------------')

            # Sleep for as long as indicated in self.loopInterval.
            time.sleep(self.loopInterval)

    def modeSelect(self):
        '''This is the method that helps the user decide what mode to run the bot in.'''
        # List of available modes.
        modes = ['test', 'prod']

        # Loop until the user has inputted a correct mode.
        while(1):
            input('Hi, I\'m Sherlock!\nIf you didn\'t mean to start me, press control + c to stop.\nPress ENTER for mode selection.\n')
            selected_mode = input('Enter "test" to run in test mode.\nEnter "prod" to run in production mode.\n')
            if selected_mode in modes:
                print(f'You entered "{selected_mode}". If this is correct, press ENTER. If not, press control + c to cancel.')
                input()
                if selected_mode == 'test':
                    return Mode.TEST
                if selected_mode == 'prod':
                    return Mode.PROD

            else: print(f'{selected_mode} is not valid mode.')

    def cleanUp(self):
        '''CleanUp crew for scraper, validator, and courier.'''
        self.scraper.cleanUp()
        self.validator.cleanUp()