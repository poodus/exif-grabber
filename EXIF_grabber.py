import os, glob
import csv
import re
from fractions import Fraction
from PIL import Image
from PIL.ExifTags import TAGS

''' EXIF GRABBER
Looks at .jpg files in a directory and returns a CSV with EXIF data from the images
EXIF data included: Date/time, flash, exposure time, ISO speed, F number
TODO make time from noon a command line flag
TODO make cmd line option to choose which variables to capture
'''

def isValidTime(hour, minute, second):
    if hour > 23 or hour < 0 or minute < 0 or minute >59 or second < 0 or second > 59:
        return 0

'''
    conv_to_time_from_noon()
    
    Converts time from the format given in the file to a time relative to noon being "0:0"
    positive values being after 12, negative values before.
'''
def conv_to_time_from_noon(input):
    hour = int(input[11:13])
    minute = int(input[14:16])
    second = int(input[17:19])
    if isValidTime(hour, minute, second) == 0:
        return "ERROR"
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
    
    Returns various EXIF data for a given file and adds to CSV row
'''
def get_exif(filename):
    print filename
    img = Image.open(filename)
    foundattributes = 0
    listbuild = []
    info = img._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        print decoded
        if decoded == 'DateTimeOriginal':
            if timeFromNoon:
                listbuild.append(conv_to_time_from_noon(str(value)))
            else:
                listbuild.append(str(value))
            foundattributes += 1
        if decoded == 'Flash':
            listbuild.append(value)
            foundattributes += 1
        if decoded == 'ExposureTime':
            input = str(value)
            # Exposure values are given as fractions. Convert them to a float.
            if '/' in input:
                list = input.split('/')
                result = int(list[0]) / int(list[1])
                listbuild.append(input)
                foundattributes += 1
            else:
                listbuild.append(input)
                foundattributes += 1
        if decoded == 'ISOSpeedRatings':
            listbuild.append(str(value))
            foundattributes += 1            
        if decoded == 'FNumber':
            input = int(value)
            listbuild.append(result)
            foundattributes += 1   
        foundattributes = 0
    return listbuild


timeFromNoon = False

'''
    main()
    
    Main application.
'''
def main():
    filesProcessed = 0
    pathToScan = raw_input("Enter file path: ")
    assert os.path.exists(pathToScan), "Not a valid directory: " + str(pathToScan)
    csvOutput = open('EXIF_table_export.csv', 'wb')
    wr = csv.writer(csvOutput)
    print "Running..."
    for currentfile in glob.glob(os.path.join(pathToScan, '*.*')):
        #if os.path.isdir(currentfile):
        #path = currentfile
        #scan_dir(path)
        if currentfile.endswith('.JPG') or currentfile.endswith('.jpg'):
            filesProcessed += 1
            attr = get_exif(currentfile)
            print attr
            wr.writerow(attr)
    print "Done! Processed " + str(filesProcessed) + " images."


main()






