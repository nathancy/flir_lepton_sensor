'''
Filename: flir_lepton_sensor.py
Description: Class to control the Flir Lepton 3 sensor 
'''

import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import time
import os

class flirLepton3Sensor(object):
    def lepton_sensor_init(self, device = "/dev/spidev0.0"):
        self.sensor = Lepton3(device)
        self.image_id = 0
        self.file_extention = ".png"
        self.path_file_name = "/home/pi/flir_lepton_sensor/scripts/path.txt"
        self.image_file_name = "/home/pi/flir_lepton_sensor/scripts/image.txt"
        self.path = self.get_path()
        self.create_image_directory()
        self.create_image_file()

    # Open text file to get path to place photos in
    def get_path(self):
        while not os.path.exists(self.path_file_name):
            time.sleep(1)
        with open(self.path_file_name, "r") as fp:
            return fp.readline()
    
    # Check if directory exists, if not then create it 
    def create_image_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create_image_file(self):
        with open(self.image_file_name, 'w') as fp:
            fp.write(str(0))
            fp.close()

    # Capture single frame
    def thermal_capture(self):
        with self.sensor as l:
            a,_ = l.capture()
        cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(a, 8, a)
        return np.uint8(a)

    # Turn recorded thermal captured frame into a image 
    def thermal_capture_record(self):
        image = self.thermal_capture()
        cv2.imwrite((self.path + "/" + str(self.image_id) + self.file_extention), image)
        self.image_id += 1

    # Write latest image ID to text file 
    def write_image_id(self):
        with open(self.image_file_name, 'w') as fp:
            fp.write(str(self.image_id))

    # Turn on ACT LED when logging
    def status_LED_enable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness > /dev/null")

    # Turn off ACT LED when not logging 
    def status_LED_disable(self):
        os.system("echo gpio | sudo tee /sys/class/leds/led0/trigger > /dev/null")
        os.system("echo 0 | sudo tee /sys/class/leds/led0/brightness > /dev/null")
