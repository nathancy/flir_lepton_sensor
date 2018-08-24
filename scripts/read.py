import time
import serial

s = serial.Serial("/dev/ttyUSB0", 115200)
while True:
    x = s.readline()
    print(x)
