'''
Filename: KML_generator.py
Description: Script to convert selected CSV data file into KML for usage with 
            Google Earth. Default resolution is every line in the CSV file (1 second). 
            Ex: Resolution = 10 means one KML point every 10 lines
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
        resolution = sys.argv[2]
    except IndexError:
        resolution = 1
    return int(resolution)

def path():
    return sys.argv[1]

kml_file_name = "image_map.kml"
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
