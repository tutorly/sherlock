from enum import Enum

class Environment(Enum):
    '''This class is simply an enum to keep track of what environment our bot is currently in. The numbers are entirely arbitrary.'''
    TEST = 0
    PROD = 1