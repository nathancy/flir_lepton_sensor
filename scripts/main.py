'''
Filename: main.py
Description: Script to run the GPS/CSV logger and image capture programs in the background 
Usage: python main.py
'''

from flir_lepton_sensor import flirLepton3Sensor
from CSV_Logger import CSV_Logger
from time import sleep
import time
from subprocess import Popen, PIPE
import sys
import os

try:
    os.system("python GPS.py &")
    time.sleep(1)
    os.system("python sensor.py &")
    '''
    GPS = Popen(['python', 'GPS.py'])
    time.sleep(1)
    Sensor = Popen(['python', 'sensor.py'])
    '''

except KeyboardInterrupt:
    print("Stopping sensor readings")
