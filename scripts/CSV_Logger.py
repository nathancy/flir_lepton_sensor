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
    # Generate directory and path to place logging file
    def GPS_logging_init(self):
        self.output_file = "data.csv"
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.directory = "photos"
        self.file_extention = ".png"
        self.timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        print(self.timestamp)
        self.path = self.directory + "/" + self.timestamp
        self.create_image_directory()
        self.create_CSV_file()
        self.create_path_file()
        self.create_image_file()
        self.clear_GPS_bus()

    # Check if directory exists, if not then create it 
    def create_image_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
   
    # Create CSV file and add column descriptions
    def create_CSV_file(self):
        self.csv_file = open(self.path + "/" + self.output_file, "w")

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

    def create_path_file(self):
        with open('path.txt', 'w') as fp:
            fp.write(self.path)
            fp.close()
    
    def create_image_file(self):
        with open('image.txt', 'w') as fp:
            fp.write(str(0))
            fp.close()

    # Read serial bus for GPS data
    def record_GPS_data(self):
        self.image_id = self.get_latest_image_id()
        msg = self.ser.readline()
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:62].strip() + "," + str(self.image_id) + "\n"
            self.csv_file.write(msg)
            print("wrote with image # " + self.image_id)

    # Return last captured image id 
    def get_latest_image_id(self):
        image_number = ""
        with open('image.txt', 'r') as image_file:
            image_number = image_file.readline()
        return image_number

    # Clear the GPS serial bus to ensure good values
    def clear_GPS_bus(self):
        for num in range(10):
            self.ser.readline()

    ###########################################
    # Debug exceptions for problems when running in background
    # Extracts failing function name from Traceback
    def setup_exception_logging(self):
        logging.basicConfig(filename="output.log",
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            )

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
