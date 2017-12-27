import os, glob
import csv
import re
from fractions import Fraction
from PIL import Image
from PIL.ExifTags import TAGS

''' 
    EXIF GRABBER
    
    Utility to analyze .jpg files in a directory and return a CSV with EXIF data from the images.

    EXIF data currently included: Date/time, flash, exposure time, ISO speed, F number

    TODO make time from noon a command line flag
    TODO make cmd line option to choose which variables to capture
    
    @author Shane Reetz (initially written in 2013, currently being rewritten)
'''

'''
    get_exif()
    
    Returns various EXIF data for a given file and adds to CSV file.
'''
def get_exif(filename):
    print filename
    img = Image.open(filename)
    foundattributes = 0
    # List to append values to
    listbuild = []
    info = img._getexif()
    # For every EXIF entry in this file...
    for tag, value in info.items():
        # Decode EXIF code into String
        decoded = TAGS.get(tag, tag)
        # Time
        if decoded == 'DateTimeOriginal':
            listbuild.append(str(value))
            foundattributes += 1
        # Flash
        elif decoded == 'Flash':
            listbuild.append(value)
            foundattributes += 1
        # Exposure
        elif decoded == 'ExposureTime':
            input = str(value)
            # Exposure values can be expressed as fractions. Convert them to a float.
            if '/' in input:
                list = input.split('/')
                result = int(list[0]) / int(list[1])
                listbuild.append(input)
                foundattributes += 1
            else:
                listbuild.append(input)
                foundattributes += 1
        # ISO
        elif decoded == 'ISOSpeedRatings':
            listbuild.append(str(value))
            foundattributes += 1
        # F Number
        elif decoded == 'FNumber':
            input = int(value)
            listbuild.append(result)
            foundattributes += 1   
        foundattributes = 0
    return listbuild

'''
    main()
    
    Main application.
    
    # TODO command line options to add: verbose mode
'''
def main():
    filesProcessed = 0
    # Get filename from user
    pathToScan = raw_input("Enter file path: ")
    # Validate directory
    try:
        assert os.path.exists(pathToScan), "Not a valid directory: " + str(pathToScan)
    except:
        print "Invalid input."
        return
    csvOutput = open('EXIF_table_export.csv', 'wb')
    wr = csv.writer(csvOutput)
    print "Running..."
    # Get the EXIF data for every JPG in the directory
    for currentfile in glob.glob(os.path.join(pathToScan, '*.*')):
        if currentfile.endswith('.JPG') or currentfile.endswith('.jpg'):
            filesProcessed += 1
            wr.writerow(get_exif(currentfile))
    print "Done. Processed " + str(filesProcessed) + " images."
    
if __name__ == "__main__":
	main()