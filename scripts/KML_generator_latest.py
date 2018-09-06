'''
Filename: KML_generator_latest.py
Description: Script to convert most recent collected CSV data in path.txt file into KML for usage with 
            Google Earth. Default resolution is every line in the CSV file (1 second). 
            Ex: Resolution = 10 means one KML point every 10 lines
Usage: python KML_generator_latest.py <resolution #>
'''

from pykml.factory import KML_ElementMaker as KML
from lxml import etree
import csv
import sys
import os 

# Convert Longtitude GPS Data (DMS -> DD)
def Longitude_DMS_to_DD(raw_longitude, direction):
    longitude_degree = int(raw_longitude/100)
    longitude_minute = raw_longitude % 100
    converted_longitude = longitude_degree + (longitude_minute/60)
    return converted_longitude if direction == "E" else -converted_longitude

# Convert Latitude GPS Data (DMS -> DD)
def Latitude_DMS_to_DD(raw_latitude, direction):
    latitude_degree = int(raw_latitude/100)
    latitude_minute = raw_latitude % 100
    converted_latitude = latitude_degree + (latitude_minute/60)
    return converted_latitude if direction == "N" else -converted_latitude

# Determines the amount of points to generate, default every point
# The higher the resolution, the less points are sampled
def resolution():
    try:
        resolution = sys.argv[1]
    except IndexError:
        resolution = 1
    return int(resolution)

# Check for CSV in path, else check for CSV in current directory
def path():
    try:
        with open(path_file_name, 'rb') as f:
            print("Found path, using CSV file in specified path")
            path = f.readline().strip()
            if not path:
                print("ERROR: Path file is empty")
                exit(1)
            else:
                full_path = path + "/" + csv_file_name
                if not os.path.exists(full_path):
                    print("ERROR: CSV file not found in specified path")
                    exit(1)
                return full_path
    except IOError:
        print("Path file does not exist, attempting to use CSV file in current directory")
        try:
            with open(csv_file_name) as f:
                print("Found CSV file in current directory")
                return csv_file_name
        except IOError: 
            print("ERROR: CSV file not found in current directory")
            exit(1)

path_file_name = 'path.txt'
kml_file_name = "image_map.kml"
csv_file_name = 'data.csv'
csv_file_path = path()

doc = KML.Folder()

with open(csv_file_path) as f:
    reader = csv.reader(f)

    # Remove column description row
    description = next(reader)
    resolution = resolution()

    for index, row in enumerate(reader):
        if index % resolution == 0:
            try:
                DMS_latitude = row[1]
                latitude_direction = row[2]
                DMS_longitude = row[3]
                longitude_direction = row[4]
                image_id = row[11]

                # Convert DMS latitude/longtitude coordinates to DD format
                DD_latitude = Latitude_DMS_to_DD(float(DMS_latitude), latitude_direction)
                DD_longitude = Longitude_DMS_to_DD(float(DMS_longitude), longitude_direction)

                # Check for invalid extra space in CSV file
                if str(DD_longitude) != "0.0" and str(DD_longitude) != "0.0":
                    # Create KML point and append to list of points
                    point = KML.Placemark(
                                KML.name(image_id),
                                KML.Point(
                                    KML.coordinates(str(DD_longitude) + "," +  str(DD_latitude)),
                                    )
                                )
                    doc.append(point)

            except IndexError:
                # Need to +2 cause CSV doesnt start and index 0 and removed description column row
                print("Note: Line #" +  str(index + 2) + " is not valid in data CSV file, aborting point")

# Turn coordinate points into .kml file
outfile = file(kml_file_name, 'w')
outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
outfile.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
outfile.write(etree.tostring(doc, pretty_print = True))
outfile.write('</kml>')
print("KML file successfully generated!")
