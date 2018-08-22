import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import datetime
import time
import os
import RPi.GPIO as GPIO

class flirLepton3Sensor(object):
    def __init__(self, device = "/dev/spidev0.0"):
        self.sensor = Lepton3(device)
        self.directory = "photos"
        self.file_extention = ".png"

    # Capture single frame
    def thermal_capture(self):
        with self.sensor as l:
            a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(a, 8, a)
        return np.uint8(a)

    # Capture single frame and record 
    def thermal_capture_record(self):
        image = self.thermal_capture()
        timestamp = str(datetime.datetime.now()).split('.')[0]
        self.create_directory(self.directory + "/" + timestamp)
        cv2.imwrite((self.directory + "/" + timestamp + "/" + self.file_extention), image)

    # Constantly record frames
    def thermal_capture_record_constant(self):
        count = 0
        timestamp = str(datetime.datetime.now()).split('.')[0]
        self.create_directory(self.directory + "/" + timestamp)
        while True:
            image = self.thermal_capture()
            cv2.imwrite((self.directory + "/" + timestamp + "/" + str(count) + self.file_extention), image)
            count += 1

    # Record frames for specific interval (seconds)
    def thermal_capture_record_interval(self, seconds):
        count = 0
        timestamp = str(datetime.datetime.now()).split('.')[0]
        self.create_directory(self.directory + "/" + timestamp)
        end_time = int(time.time()) + seconds
        while int(time.time()) < end_time:
            image = self.thermal_capture()
            cv2.imwrite((self.directory + "/" + timestamp + "/" + str(count) + self.file_extention), image)
            count += 1
   
    # Gets current time stamp 
    def current_timestamp(self):
        return str(datetime.datetime.now()).split('.')[0]
        #return datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S")

    # Check if directory exists, if not then create it 
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def status_LED_enable(self):

        # The green ACT LED (led0) has triggers which let some other part of the kernel control the LED. The default trigger for the LED is 'mmc0' which actives when the SD card is accessed. Therese two lines deactivate the mmc0 trigger. GPIO16 can be used to control the LED, its active-low so to turn the LED on, set the pin low, and to turn the LED off, set the pin high. 

        # It's important to note that RPi.GPIO will set the GPIO port to be an input when it's finished (it sets to an input any port which the script set to an output, and you have to set it to an output before you can do anything with it, even if it already was). As GPIO16 stops being an output, control via the kernel interface will no longer work.
        #os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        #os.system("echo cpu0 | sudo tee /sys/class/leds/led0/trigger > /dev/null")

        # Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
        # connector pin number, and the LED GPIO isn't on the connector
        #GPIO.setmode(GPIO.BCM)

        # Set up GPIO output channel
        #GPIO.setup(16, GPIO.OUT)
       
        # On
        #GPIO.output(16, GPIO.LOW)   
        #GPIO.cleanup()
        
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null")

    def status_LED_disable(self):
        #os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        #os.system("echo cpu0 | sudo tee /sys/class/leds/led0/trigger > /dev/null")

        # Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
        # connector pin number, and the LED GPIO isn't on the connector
        #GPIO.setmode(GPIO.BCM)

        # Set up GPIO output channel
        #GPIO.setup(16, GPIO.OUT)
       
        # Off
        #GPIO.output(16, GPIO.HIGH)   

        #GPIO.cleanup()
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null")
