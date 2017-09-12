import os, glob
import csv
import re
from fractions import Fraction
from PIL import Image
from PIL.ExifTags import TAGS

''' EXIF GRABBER
Looks at .jpg files in a directory and returns a CSV with EXIF data from the images
EXIF data included: Date/time, flash, exposure time (shutter speed), ISO speed, F number
TODO Ask user for directory input
TODO make time from noon a command line flag
TODO make cmd line option to choose which variables to capture
'''

def isValidTime(hour, minute, second):
    if hour > 23 or hour < 0 or minute < 0 or minute >59 or second < 0 or second > 59:
        return 0

# Converts time from the format given in the file to a time relative to noon being "0:0"
# positive values being after 12, negative values before

def conv_to_time_from_noon(input):
    hour = int(input[11:13])
    minute = int(input[14:16])
    second = int(input[17:19])
    if isValidTime(hour, minute, second) ==0:
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


#Run for each file
# Returns various EXIF data and adds to CSV row
def get_exif(filename):
    img = Image.open(filename)
    foundattributes = 0
    listbuild = []
    info = img._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        if decoded == 'DateTimeOriginal':
            listbuild.append(conv_to_time_from_noon(str(value)))
            foundattributes += 1
        if decoded == 'Flash':
            listbuild.append(value)
            foundattributes += 1
        if decoded == 'ExposureTime':
            input = str(value)
            # Exposure values are given as fractions. Convert them to a float.
            result = float(sum(Fraction(s) for s in (re.sub(r',\s', '/', input[1:-1])).split()))
            listbuild.append(input)
            foundattributes += 1
        if decoded == 'ISOSpeedRatings':
            #print 'ISO: ' + str(value)
            listbuild.append(str(value))
            foundattributes += 1            
        if decoded == 'FNumber':
            input = str(value)
            # F numbers are given as fractions. Convert them to a float.
            result = float(sum(Fraction(s) for s in (re.sub(r',\s', '/', input[1:-1])).split()))
            listbuild.append(result)
            foundattributes += 1   
        if foundattributes == 5:
            wr.writerow(listbuild)
            foundattributes=0

# Finds each file to run get_exif on
def scan_dir(path):
    print "Running..."
    for currentfile in glob.glob( os.path.join(path, '*.*')):
        #if os.path.isdir(currentfile):
            #path = currentfile
            #scan_dir(path)
        if currentfile.endswith('.JPG') or currentfile.endswith('.jpg'):
            #print 'Current file: ' + currentfile
            get_exif(currentfile)
    print "Done!"

def main():
    pathToScan = raw_input("Enter file path: ")
    assert os.path.exists(pathToScan), "Not a valid directory: " + str(pathToScan)
    csvOutput = open('EXIF_table_export.csv', 'wb')
    wr = csv.writer(csvOutput)
    scan_dir(pathToScan)

main()






