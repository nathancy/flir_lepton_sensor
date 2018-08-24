import serial
import os
import datetime
import time

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
        #print(image_id)
        msg = self.ser.readline()
        if msg[:7] == "$GPGGA,":
            print(msg[:7])
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:].strip() + "," + str(image_id) + "\n"
            print(msg)
            self.csv_file.write(msg)

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
   

