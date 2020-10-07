from enum import Enum

class Mode(Enum):
    '''This class is simply an enum to keep track of what mode our bot is currently in. The numbers are entirely arbitrary.'''
    TEST = 0
    PROD = 1