'''
Filename: CSV_logger.py
Description: Class to log data into a CSV file 
'''

import serial
import os
import time
import logging
import traceback
import sys
from time import sleep

class CSV_Logger(object):
    # Generate directory and path to place logging file
    def GPS_logging_init(self):
        self.ser = serial.Serial("/dev/ttyAMA0")
        self.directory = "/home/pi/flir_lepton_sensor/scripts/photos"
        self.output_file_name = "data.csv"
        self.path_file_name = "/home/pi/flir_lepton_sensor/scripts/path.txt"
        self.image_file_name = "/home/pi/flir_lepton_sensor/scripts/image.txt"
        self.file_extention = ".png"
        self.remove_old_logging_files()
        self.timestamp = self.get_GPS_timestamp()
        self.clear_GPS_bus()
        print(self.timestamp)
        '''
        try:
            with open('timestamp.txt', 'w') as fp:
                fp.write(self.timestamp)
                fp.write('\n')
                fp.write('\n')
                for x in range(10):
                    fp.write(self.get_GPS_timestamp() +'\n')
                    #time.sleep(1)
        except IOError:
            fp.write('Failed')
        '''
        self.path = self.directory + "/" + self.timestamp
        self.create_image_directory()
        self.create_CSV_file()
        self.create_path_file()
        self.create_image_file()
  
    # Since Raspberry Pi does not have RTC, it uses last saved timestamp on power outage which can be 
    # very inaccurate. So we use the GPS's UTC time from the GPGGA field and the date from the GPRMC field
    # as the current time stamp. In addition, the only way to get reliable timestamp without a internet connection
    # is using GPS or a RTC so thats why we use GPS for current date/timestamp. Datasheet:
    # https://cdn.sparkfun.com/datasheets/Sensors/GPS/Venus/638/doc/Venus638FLPx_DS_v07.pdf
    def get_GPS_timestamp(self):
        date = self.get_UTC_date()
        while date[-2:] == '06':
            date = self.get_UTC_date()

        msg = self.ser.readline()
        # Get UTC time
        while msg[:7] != "$GPGGA,":
            msg = self.ser.readline()
        UTC_time = msg[7:13]
        timestamp = date + "_" + UTC_time 
        return timestamp

    def get_UTC_date(self):
        msg = self.ser.readline()
        while msg[:7] != "$GPRMC,":
            msg = self.ser.readline()
        l = [x.strip() for x in msg[7:].split(",")]
        UTC_date_day = l[8][:2]
        UTC_date_month = l[8][2:4]
        UTC_date_year = l[8][4:]
        date = UTC_date_month + "_" + UTC_date_day + "_" + "20" + UTC_date_year
        return date
        
    def remove_old_logging_files(self):
        try:
            os.remove(self.path_file_name)
            os.remove(self.image_file_name)
        except OSError:
            pass

    # Check if directory exists, if not then create it 
    def create_image_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
   
    # Create CSV file and add column descriptions
    def create_CSV_file(self):
        with open(self.path + "/" + self.output_file_name, "w") as fp:
            fp.write("UTC Time,")
            fp.write("Latitude,")
            fp.write("North/South Indicator,")
            fp.write("Longitude,")
            fp.write("East/West Indicator,")
            fp.write("GPS Quality Indicator,")
            fp.write("Satellites Used,")
            fp.write("HDOP,")
            fp.write("Altitude,")
            fp.write("DGPS Station ID,")
            fp.write("Checksum,")
            fp.write("Image ID\n")
            fp.close()

    def create_path_file(self):
        with open(self.path_file_name, 'w') as fp:
            fp.write(self.path)
            fp.close()
    
    def create_image_file(self):
        with open(self.image_file_name, 'w') as fp:
            fp.write(str(0))
            fp.close()

    # Read serial bus for GPS data
    def record_GPS_data(self):
        self.image_id = self.get_latest_image_id()
        # Ensure image_id is not blank
        if self.image_id.isdigit():
            msg = self.ser.readline()
            while msg[:7] != "$GPGGA,":
                msg = self.ser.readline()
            if '\0' not in msg and msg[:7] == "$GPGGA,":
                l = [x.strip() for x in msg[7:].split(",")]
                # Ensure GPS Quality indicator is not 0 (position fix unavailable)
                if l[5] != '0':
                    # Grab all fields from 1-11 on datasheet
                    msg = ",".join(l[:11]) + "," + str(self.image_id) + "\n"
                    with open(self.path + "/" + self.output_file_name, "a") as fp:
                        fp.write(msg)
                    print("wrote with image # " + self.image_id)

    # Return last captured image id 
    def get_latest_image_id(self):
        image_number = ""
        with open(self.image_file_name, 'r') as image_file:
            image_number = image_file.readline().strip()
            if image_number.isdigit():
                return image_number
            else:
                return str(-1)

    # Clear the GPS serial bus to ensure good values
    def clear_GPS_bus(self):
        for num in range(30):
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
