import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import datetime
import time
import os

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
