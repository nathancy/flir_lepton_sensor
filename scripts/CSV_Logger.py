import serial
import os
import datetime
import time
from time import sleep

class CSV_Logger(object):
    def __init__(self):
        self.output_file = "data.csv"
        self.path_file = "path.txt"
        self.image_file = "image.txt"
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.directory = "photos"
        self.file_extention = ".png"
        self.timestamp = ""
        self.path = ""

    def GPS_logging_init(self):
        self.timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H%M%S")
        self.path = self.directory + "/" + self.timestamp
        self.create_directory()
        self.create_CSV_headers()
        self.create_path_and_image_files()
        self.clear()

    # Check if directory exists, if not then create it 
    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
   
    def create_CSV_headers(self):
        # Write column description names
        self.csv_file = open(self.path + "/" + self.output_file, "w+")

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

    def create_path_and_image_files(self):
        path_file = open(self.path_file, 'w')
        path_file.write(self.path)
        image_file = open(self.image_file, 'w')

    def record_GPS_data(self, image_id):
        msg = self.ser.readline()
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:62].strip() + "," + str(image_id) + "\n"
            self.csv_file.write(msg)

    def clear(self):
        for num in range(10):
            self.ser.readline()

    def get_path(self):
        return self.path

    # Seconds
    def time_passed(self, old_time, duration):
        length = time.time() - old_time
        while length < duration:
            length = time.time() - old_time
        return True    

    def get_latest_image_id(self):
        if os.stat(self.image_file).st_size == 0:
            return 0
        else:
            fileHandle = open(self.image_file, "r")
            last_line = fileHandle.readlines()[-1]
            fileHandle.close()
            return last_line.strip()
