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
        self.image_id = 0
        self.file_extention = ".png"
        self.path_file = "/home/pi/flir_lepton_sensor/scripts/path.txt"
        self.image_file = "/home/pi/flir_lepton_sensor/scripts/image.txt"
        self.path = ""

    # Capture single frame
    def thermal_capture(self):
        with self.sensor as l:
            a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(a, 8, a)
        return np.uint8(a)

    # Constantly record frames and record data to CSV file
    def thermal_capture_record_constant_CSV_logging(self):
        image = self.thermal_capture()
        cv2.imwrite((self.path + "/" + str(self.image_id) + self.file_extention), image)
        self.image_id += 1

    def get_image_id(self):
        return self.image_id

    # Gets current time stamp 
    def current_timestamp(self):
        return datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
    
    def set_path(self):
        try:
            with open(self.path_file, "rb") as f:
                self.path = f.readline()
        except IOError:
            time.sleep(10)
            with open(self.path_file, "rb") as f:
                self.path = f.readline()

    
    # Check if directory exists, if not then create it 
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def write_image_id(self):
        fileHandle = open(self.image_file, 'w')
        fileHandle.write(str(self.image_id) + "\n")

    # Turn on ACT LED when logging
    def status_LED_enable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null")

    # Turn off ACT LED when not logging 
    def status_LED_disable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null")
