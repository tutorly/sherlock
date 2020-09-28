import time


def incrementCases():
    """
    This function will read the cases.txt file and increase it's value by one.
    """
    f = open('cases.txt')
    count = f.read()
    count = int(count) + 1
    f.close()
    f = open('cases.txt', 'w')
    f.write(str(count))
    f.close()


def getCurrentCases():
    """
    This function will read cases.txt and return the count.
    """
    f = open('cases.txt')
    count = f.read()
    f.close()
    return count
