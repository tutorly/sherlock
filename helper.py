import time


def incrementCases():
    """
    This function will read the .txt file and increase it's value by one. 
    It is to be used whenever we have found a new COVID-19 case on campus
    """
    f = open('cases.txt')
    count = f.read()
    count = int(count) + 1
    f.close()
    f = open('cases.txt', 'w')
    f.write(str(count))
