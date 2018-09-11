'''
Filename: CSV_logger.py
Description: Class to log data into a CSV file 
'''

import serial
import os
import datetime
import time
import logging
import traceback
import sys
from time import sleep

class CSV_Logger(object):
    def __init__(self):
        self.output_file = "data.csv"
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.directory = "photos"
        self.file_extention = ".png"

    # Generate directory and path to place logging file
    def GPS_logging_init(self):
        self.timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        self.path = self.directory + "/" + self.timestamp
        self.create_directory(self.path)
        self.generate_CSV_file(self.path)
        self.clear_GPS_bus()

    # Create CSV file and add column descriptions
    def generate_CSV_file(self, path):
        self.csv_file = open(path + "/" + self.output_file, "w+")

        self.csv_file.write("UTC Time,")
        self.csv_file.write("Latitude,")
        self.csv_file.write("North/South Indicator,")
        self.csv_file.write("Longitude,")
        self.csv_file.write("East/West Indicator,")
        self.csv_file.write("GPS Quality Indicator,")
        self.csv_file.write("Satellites Used,")
        self.csv_file.write("HDOP,")
        self.csv_file.write("Altitude,")
        self.csv_file.write("DGPS Station ID,")
        self.csv_file.write("Checksum,")
        self.csv_file.write("Image ID\n")

    # Read serial bus for GPS data
    def record_GPS_data(self, image_id):
        msg = self.ser.readline()
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:62].strip() + "," + str(image_id) + "\n"
            self.csv_file.write(msg)
            #print("wrote")

    # Clear the GPS serial bus to ensure good values
    def clear_GPS_bus(self):
        for num in range(10):
            self.ser.readline()

    # Retrieve path of logging file
    def get_path(self):
        return self.path

    # Check if directory exists, if not then create it 
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
   
    # Check how many seconds have passed
    def time_passed(self, old_time, duration):
        length = time.time() - old_time
        while length < duration:
            length = time.time() - old_time
        return True    

    # Place path and image files
    def create_path_and_image_file(self, path):
        path_file= open('path.txt', 'w')
        path_file.write(path)
        image_file = open('image.txt', 'w')

    # Return last captured image id 
    def get_latest_image_id(self):
        if os.stat("image.txt").st_size == 0:
            return 0
        else:
            fileHandle = open("image.txt", "r")
            last_line = fileHandle.readlines()[-1]
            fileHandle.close()
            return last_line.strip()

    def setup_exception_logging(self):
        logging.basicConfig(filename="output.log",
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            )

    ###########################################
    # Debug exceptions for problems when running in background
    # Extracts failing function name from Traceback
    def extract_function_name(self):
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 1)
        fname = stk[0][3]
        return fname

    def log_exception(self, e):
        print("Error: Checkout output log")
        logging.error(
        "Function {function_name} raised {exception_class} ({exception_docstring}): {exception_message}".format(
        function_name = self.extract_function_name(), #this is optional
        exception_class = e.__class__,
        exception_docstring = e.__doc__,
        exception_message = e.message))
