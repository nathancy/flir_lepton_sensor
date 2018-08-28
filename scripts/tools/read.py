'''
Filename: read.py
Description: Read data from serial bus 
Usage: python read.py 
'''
import serial

s = serial.Serial("/dev/ttyAMA0")
while True:
    x = s.readline()
    print(x)
