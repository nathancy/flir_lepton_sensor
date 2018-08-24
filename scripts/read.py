import time
import serial

s = serial.Serial("/dev/ttyAMA0")
while True:
    x = s.readline()
    print(x)
