'''
Filename: GPS.py
Description: Script to constantly log current GPS coordinates into a CSV file with the corresponding 
             thermal image ID. Used together with sensor.py
Usage: python GPS.py
'''

from CSV_Logger import CSV_Logger
import os 
import time

logger = CSV_Logger()
logger.GPS_logging_init()
path = logger.get_path()
logger.create_directory(path)
logger.create_path_and_image_file(path)

try:
    while True:
        image_id = logger.get_latest_image_id()
        logger.record_GPS_data(image_id)
except KeyboardInterrupt:
    print("stopped logging")



