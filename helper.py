import time

def incrementCount():
    f = open('cases.txt')
    count = f.read()
    count = int(count) + 1
    f.close()
    f = open('count.txt', 'w')
    f.write(str(count))


for x in range(0,100):
    incrementCount()
    time.sleep(1)

