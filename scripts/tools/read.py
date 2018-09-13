'''
Filename: read.py
Description: Read data from serial bus 
Usage: python read.py 
'''
import serial

def get_GPS_timestamp():
    msg = s.readline()
    # Get UTC time
    while msg[:7] != "$GPGGA,":
        msg = s.readline()
    UTC_time = msg[7:13]
    msg = s.readline()
    # Get UTC date
    while msg[:7] != "$GPRMC,":
        msg = s.readline()
    l = [x.strip() for x in msg[7:].split(",")]
    UTC_date_day = l[8][:2]
    UTC_date_month = l[8][2:4]
    UTC_date_year = l[8][4:]
    date = UTC_date_month + "_" + UTC_date_day + "_" + "20" + UTC_date_year
    timestamp = date + "_" + UTC_time 
    print(timestamp)
    

s = serial.Serial("/dev/ttyAMA0")
while True:
    x = s.readline()
    print(x)
    #get_GPS_timestamp()
