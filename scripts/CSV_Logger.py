import serial

class CSV_Logger(object):
    def initialize(self, path):
        self.output_file = "data.csv"
        self.csv_file = open(path + "/" + self.output_file, "w+")
        self.ser = serial.Serial("/dev/ttyAMA0")

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

    def record_GPS_data(self, image_id):
        msg = self.ser.readline()
        print(msg[:7])
        if '\0' not in msg and msg[:7] == "$GPGGA,":
            msg = msg[7:].strip() + "," + str(image_id) + "\n"
            print(msg)
            self.csv_file.write(msg)

    def clear(self):
        for num in range(10):
            self.ser.readline()


