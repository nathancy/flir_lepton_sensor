from flir_lepton_sensor import flirLepton3Sensor
from CSV_Logger import CSV_Logger
from time import sleep
import time
from subprocess import Popen, PIPE
import sys

try:
    GPS = Popen(['python', 'GPS.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    Sensor = Popen(['python', 'sensor.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    '''
    # Read in path from GPS.py
    out,_ = GPS.communicate()
    print(GPS.communicate(out.decode().strip()))

    
    # Give path to sensor



    #sensor_led.status_LED_enable()
    '''
except KeyboardInterrupt:
    print("Stopping sensor readings")
    #sensor_led.status_LED_disable()
