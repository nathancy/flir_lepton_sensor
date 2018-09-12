'''
Filename: clean.py
Description: Script to clean up temporary .txt files, photos, and output debug logs 
'''

import os 
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/path.txt")
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/image.txt")
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/*.pyc")
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/photos")
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/output.log")
os.system("sudo rm -rf /home/pi/flir_lepton_sensor/scripts/image_map.kml")
