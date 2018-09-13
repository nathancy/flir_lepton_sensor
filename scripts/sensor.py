#!/usr/bin/python
'''
Filename: sensor.py
Description: Script to constantly capture thermal images using the Flir Lepton 3 
Usage: python sensor.py
'''

from flir_lepton_sensor import flirLepton3Sensor
from time import sleep

try:
    sensor = flirLepton3Sensor()
    sensor.lepton_sensor_init()
    #sensor.status_LED_enable()
    while True:
        sensor.thermal_capture_record()
        sensor.write_image_id()
except KeyboardInterrupt:
    #sensor.status_LED_disable()
    print("stopping photo capture")

