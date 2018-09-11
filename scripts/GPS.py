'''
Filename: GPS.py
Description: Script to constantly log current GPS coordinates into a CSV file with the corresponding 
             thermal image ID. Used together with sensor.py
Usage: python GPS.py
'''

from CSV_Logger import CSV_Logger
import os 
import time
import exceptions

try:
    logger = CSV_Logger()
    logger.GPS_logging_init()
    try:
        while True:
            logger.record_GPS_data()
    except KeyboardInterrupt:
        print("stopped logging")
except exceptions.Exception as e:
    logger.setup_exception_logging()
    logger.log_exception(e)

