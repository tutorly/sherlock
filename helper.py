def incrementCount():
    f = open('count.txt', 'w')
    f.truncate(0)
    f.close()


incrementCount()
