import multiprocessing
from time import sleep
import time
import os
import csv

def capture(num):
    sleep(.1)
    open("photos/" + str(num) + ".txt", "a+")
    print("created file")

def logger(num):
    with open("photos/output.csv", "a+") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([num])
        print("wrote")
        sleep(1)

# Seconds
def time_passed(old_time, duration):
    length = time.time() - old_time
    while length < duration:
        length = time.time() - old_time
    return True    

def create_dir():
    if not os.path.exists("photos"):
        os.makedirs("photos")

create_dir()
csv_file = open("photos/output.csv", "w+")

if __name__ == '__main__':
    i = 0
    while True:
        # make capture daemon?
        multiprocessing.Process(target=capture, args=(i,)).start()
        '''
        a = multiprocessing.Process(target=capture, args=(i,))
        a.daemon = True
        a.start()
        '''

        log = multiprocessing.Process(target=logger, args=(i,))
        log.start()
        i += 1
        while log.is_alive():
            multiprocessing.Process(target=capture, args=(i,)).start()
            '''
            b = multiprocessing.Process(target=capture, args=(i,))
            b.daemon = True
            b.start()
            '''
            i += 1
