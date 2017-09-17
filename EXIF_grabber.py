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
    conv_to_time_from_noon()
    
    Converts time from the format given in the file to a time relative to noon being "0:0"
    positive values being after 12, negative values before. This was useful in the initial
    use case of this project, for statistical analysis of time values in relation to exposure.
'''
def conv_to_time_from_noon(input):
    # Get values from input.
    hour = int(input[11:13])
    minute = int(input[14:16])
    second = int(input[17:19])
    # Case 1: After Noon
    if hour >= 12 and hour <=23:
        hour = hour - 12
        return str(hour) + ":" + str(minute) + ":" + str(second)
    # Case 2: Before Noon
    if hour < 12 and hour >= 0:
        carry_s = 0
        carry_m = 0
        if second!=0:
            carry_s = 1
            second = 60-second
        if minute!=0:
            carry_m = 1
            minute = 60-minute-carry_s
            hour = 12 - hour - carry_m
        else: hour = 12 - hour
    return str(hour) + ":" + str(minute) + ":" + str(second)

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
            if timeFromNoon:
                listbuild.append(conv_to_time_from_noon(str(value)))
            else:
                listbuild.append(str(value))
            foundattributes += 1
        # Flash
        if decoded == 'Flash':
            listbuild.append(value)
            foundattributes += 1
        # Exposure
        if decoded == 'ExposureTime':
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
        if decoded == 'ISOSpeedRatings':
            listbuild.append(str(value))
            foundattributes += 1
        # F Number
        if decoded == 'FNumber':
            input = int(value)
            listbuild.append(result)
            foundattributes += 1   
        foundattributes = 0
    return listbuild

# Flag for using this option.
timeFromNoon = False

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
    # For every file in the directory, analyze its EXIF data
    for currentfile in glob.glob(os.path.join(pathToScan, '*.*')):
        if currentfile.endswith('.JPG') or currentfile.endswith('.jpg'):
            filesProcessed += 1
            wr.writerow(get_exif(currentfile))
    print "Done! Processed " + str(filesProcessed) + " images."

main()






