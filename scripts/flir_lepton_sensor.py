import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import datetime
import time
import os
import RPi.GPIO as GPIO
from CSV_Logger import CSV_Logger

class flirLepton3Sensor(object):
    def __init__(self, device = "/dev/spidev0.0"):
        self.sensor = Lepton3(device)
        self.directory = "photos"
        self.file_extention = ".png"
        self.logger = CSV_Logger()

    # Capture single frame
    def thermal_capture(self):
        with self.sensor as l:
            a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(a, 8, a)
        return np.uint8(a)

    # Capture single frame and record that frame
    def thermal_capture_record(self):
        image_id = 0
        timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        path = self.directory + "/" + timestamp
        self.create_directory(path)
        self.logger.initialize(path)
        self.logger.clear()
        image = self.thermal_capture()
        cv2.imwrite((path + "/" + str(image_id) + self.file_extention), image)
        self.logger.record(image_id)

    # Constantly record frames
    def thermal_capture_record_constant(self):
        image_id = 0
        timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        path = self.directory + "/" + timestamp
        self.create_directory(path)
        self.logger.initialize(path)
        self.logger.clear()
        while True:
            image = self.thermal_capture()
            cv2.imwrite((path + "/" + str(image_id) + self.file_extention), image)
            self.logger.record(image_id)
            image_id += 1

    # Record frames for specific interval (seconds)
    def thermal_capture_record_interval(self, seconds):
        image_id = 0
        timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        path = self.directory + "/" + timestamp
        self.create_directory(path)
        self.logger.initialize(path)
        self.logger.clear()
        end_time = int(time.time()) + seconds
        while int(time.time()) < end_time:
            image = self.thermal_capture()
            cv2.imwrite((path + "/" + str(image_id) + self.file_extention), image)
            self.logger.record(image_id)
            image_id += 1
   
    # Gets current time stamp 
    def current_timestamp(self):
        return datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")

    # Check if directory exists, if not then create it 
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def status_LED_enable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null")

    def status_LED_disable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null")
