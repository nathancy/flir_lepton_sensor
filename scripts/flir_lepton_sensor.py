import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3
import datetime
import time


class flirLepton3Sensor(object):
    def __init__(self, device = "/dev/spidev0.0"):
        self.sensor = Lepton3(device)
        self.directory = "photos"
        self.file_extention = ".jpg"

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
        cv2.imwrite((self.directory + "/" + str(self.current_timestamp()) + self.file_extention), image)

    # Constantly record frames
    def thermal_capture_record_constant(self):
        while True:
            image = self.thermal_capture()
            cv2.imwrite((self.directory + "/" + str(self.current_timestamp()) + self.file_extention), image)

    # Record frames for specific interval (seconds)
    def thermal_capture_record_interval(self, seconds):
        end_time = int(time.time()) + seconds
        while int(time.time()) < end_time:
            self.thermal_capture_record()
   
    # Gets current time stamp 
    def current_timestamp(self):
        return datetime.datetime.now().strftime("%m_%d_%Y::%H_%M_%S")
