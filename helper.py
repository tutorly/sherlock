import time

def incrementCases():
    f = open('cases.txt')
    count = f.read()
    count = int(count) + 1
    f.close()
    f = open('count.txt', 'w')
    f.write(str(count))


for x in range(0,100):
    incrementCases()
    time.sleep(1)

