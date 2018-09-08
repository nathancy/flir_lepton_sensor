from CSV_Logger import CSV_Logger
import os 
import time

logger = CSV_Logger()
logger.GPS_logging_init()

try:
    while True:
        image_id = logger.get_latest_image_id()
        logger.record_GPS_data(image_id)
except KeyboardInterrupt:
    print("stopped logging")


