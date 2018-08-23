import serial

class CSV_Logger(object):
    def initialize(self, path):
        self.csv_file = open(path + "/" +  "data.csv", "w+")
        self.ser = serial.Serial("/dev/ttyUSB0", 115200)

        # Write column description names
        self.csv_file.write("UTC Time,")
        self.csv_file.write("Latitude,")
        self.csv_file.write("North/South Indicator,")
        self.csv_file.write("Longitude,")
        self.csv_file.write("East/West Indicator,")
        self.csv_file.write("GPS Quality Indicator,")
        self.csv_file.write("Satellites Used,")
        self.csv_file.write("HDOP,")
        self.csv_file.write("Altitude,")
        self.csv_file.write("DGPS Station ID,")
        self.csv_file.write("Checksum,")
        self.csv_file.write("Image ID\n")

    def record(self, image_id):
        msg = self.ser.readline().strip() + "," + str(image_id) + "\n"
        self.csv_file.write(msg)


