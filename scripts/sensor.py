'''
Filename: sensor.py
Description: Script to constantly capture thermal images using the Flir Lepton 3 
Usage: python sensor.py
'''

from flir_lepton_sensor import flirLepton3Sensor
from time import sleep

sensor = flirLepton3Sensor()

try:
    sleep(1)
    sensor.status_LED_enable()
    path = sensor.get_path()
    sensor.create_directory(path)
    while True:
        sensor.thermal_capture_record(path)
        sensor.write_image_id()
except KeyboardInterrupt:
    sensor.status_LED_disable()
    print("stopping photo capture")

