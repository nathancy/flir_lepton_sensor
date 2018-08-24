import time
import serial
s = serial.Serial("/dev/ttyUSB1", 115200)

UTC_Time = "001122.333"
Latitude = "1234.1234"
NS_Indicator = "N"
Longitude = "12310.5522"
EW_Indicator = "E"
GPS_Quality_Indicator = "1"
Satellites_Used = "11"
HDOP = "0.8"
Altitude = "108.2"
DGPS_Station_ID = "0000"
Checksum = "02"

while True:
    msg = UTC_Time + "," + Latitude + "," + NS_Indicator + "," + Longitude + "," + EW_Indicator + "," + GPS_Quality_Indicator + "," + Satellites_Used + "," + HDOP + "," + Altitude + "," + DGPS_Station_ID + "," + Checksum + "\n"
    s.write(msg)
    time.sleep(.1)
