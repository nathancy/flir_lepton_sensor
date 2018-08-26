import serial
import os
import datetime
import time
from time import sleep

class CSV_Logger(object):
    def __init__(self):
        self.output_file = "data.csv"
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.directory = "photos"
        self.file_extention = ".png"
        self.timestamp = ""
        self.path = ""

    def initialize(self, path):
        # Write column description names
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

    def record_GPS_data(self, image_id):
        '''
        msg = self.ser.readline()
        if msg[:7] == "$GPGGA,":
            msg = msg[7:].strip() + "," + str(image_id) + "\n"
            self.csv_file.write(msg)
            print('wrote')

        '''
        msg = self.ser.readline()
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:62].strip() + "," + str(image_id) + "\n"
            self.csv_file.write(msg)
            print("wrote")

    def clear(self):
        for num in range(10):
            self.ser.readline()

    def GPS_logging_init(self):
        self.timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        self.path = self.directory + "/" + self.timestamp
        self.create_directory(self.path)
        self.initialize(self.path)
        self.clear()
    def get_path(self):
        return self.path

    # Check if directory exists, if not then create it 
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
   
    # Seconds
    def time_passed(self, old_time, duration):
        length = time.time() - old_time
        while length < duration:
            length = time.time() - old_time
        return True    

    def create_path_and_image_file(self, path):
        path_file= open('path.txt', 'w')
        path_file.write(path)
        image_file = open('image.txt', 'w')

    def get_latest_image_id(self):
        if os.stat("image.txt").st_size == 0:
            return 0
        else:
            fileHandle = open("image.txt", "r")
            last_line = fileHandle.readlines()[-1]
            fileHandle.close()
            return last_line.strip()
