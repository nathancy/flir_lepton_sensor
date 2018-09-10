import serial
import os
import datetime
import time
from time import sleep

class CSV_Logger(object):
    def __init__(self):
        self.output_file = "data.csv"
        self.path_file = "/home/pi/flir_lepton_sensor/scripts/path.txt"
        self.image_file = "/home/pi/flir_lepton_sensor/scripts/image.txt"
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.CSV_data_file = ""
        self.directory = "/home/pi/flir_lepton_sensor/scripts/photos"
        self.file_extention = ".png"
        self.timestamp = ""
        self.path = ""

    def GPS_logging_init(self):
        self.remove_previous_sessions()
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
        self.CSV_data_file = self.path + "/" + self.output_file
        with open(self.CSV_data_file, "w+") as csv_file:
            csv_file.write("UTC Time,")
            csv_file.write("Latitude,")
            csv_file.write("North/South Indicator,")
            csv_file.write("Longitude,")
            csv_file.write("East/West Indicator,")
            csv_file.write("GPS Quality Indicator,")
            csv_file.write("Satellites Used,")
            csv_file.write("HDOP,")
            csv_file.write("Altitude,")
            csv_file.write("DGPS Station ID,")
            csv_file.write("Checksum,")
            csv_file.write("Image ID\n")

    def create_path_and_image_files(self):
        path_file = open(self.path_file, 'w')
        path_file.write(self.path)
        image_file = open(self.image_file, 'w')

    def remove_previous_sessions(self):
        os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/path.txt")
        os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/image.txt")

    def record_GPS_data(self, image_id):
        msg = self.ser.readline()
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:62].strip() + "," + str(image_id) + "\n"
            with open(self.CSV_data_file, "a+") as csv_file:
                csv_file.write(msg)

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
            try:
                fileHandle = open(self.image_file, "r")
                last_line = fileHandle.readlines()[-1]
                fileHandle.close()
                return last_line.strip()
            except IndexError:
                return 0
