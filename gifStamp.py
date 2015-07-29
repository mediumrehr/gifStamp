#########################################################################
# 
#  File: gifStamp.py
#  Author: Rob Rehr
#  Description: A python script for creating animated gifs from images
#    taken within a defined time of each other, based on the EXIF data
#    timestamp. gifStamp should be placed in the same directory as the
#    the collection of jpg images that this script should be used with.
#
#  Command format: python gifStamp.py [[[time_delta] dither] gif_name]
#  - By default, time is 10s, dither is 10, and gif name is 'GIF'.
#  Examples:
#    python gifStamp.py
#    python gifStamp.py 15
#    python gifStamp.py 15 20
#    python gifStamp.py 15 20 myGif
#
#  Dependencies:
#  - ExifRead 2.1.1
#  - images2gif 1.0.1
#  - PILLOW 2.9.0
#
#  License: Beerware. Feel free to use it, with or without attribution,  
#    in your own projects. If you find it helpful, buy me a beer next
#    time you see me at the local pub.
#
#########################################################################

import exifread
from images2gif import writeGif
from PIL import Image
from datetime import datetime
import os, sys

imgDic = {}     # Dictionary that holds image file names, keyed by date and time taken
dateArray = []  # Array of dates and times used as keys for imgDic
dateSorted = [] # Array of sorted image dates and times
gifDates = []   # Array of grouped date dictionary indices for gifs
timeDelta = 10  # Default to 10 seconds
dither = 10		# Default to 10
gifName = "GIF" # Default to "GIF"

# Get max time difference for images in groups from first argument
if (len(sys.argv) > 1):
	if ((sys.argv[1].isdigit()) and (sys.argv[1] > 0)):
		timeDelta = int(sys.argv[1]) # Set time delta to first argument if it's an integer greater than 0
	else:
		print "Please use command format::
		print "python gifStamp.py [[[time_delta] dither] gif_name]"
		sys.exit()

# Get gif file name from second argument
if (len(sys.argv) > 2):
	if ((sys.argv[2].isdigit()) and (sys.argv[2] >= 0)):
		dither = int(sys.argv[1]) # Set dither to second argument if it's an integer greater or equal to 0
	else:
		print "Please use command format::
		print "python gifStamp.py [[[time_delta] dither] gif_name]"
		sys.exit()
	
# Get gif file name from second argument
if (len(sys.argv) > 3):
	gifName = sys.argv[3] # Set the gif name to third argument if was specified	
	
print "Getting EXIF data from images..."

# For each file that contains '.JPG' in the current directory,
# get the date the picture was taken from the EXIF data, add
# the file name to imgDic with the date and time as the key,
# and store the date and time as a datetime object in dateArray
for filename in os.listdir(os.getcwd()):
	if ".JPG" in filename:
		f = open(filename, 'rb') # Open the 
		tags = exifread.process_file(f) # Get EXIF data
		tag = "%s" % tags['EXIF DateTimeOriginal'] # Get the date and time from EXIF data
		imgDic[tag.replace(":","").replace(" ","")] = f.name # Add file name to imgDic with date and time as key
		dateArray.append(datetime.strptime(tag, "%Y:%m:%d %H:%M:%S")) # Add datetime object to dateArray
		f.close() # Close the file

print "Sorting datetimes..."
dateSorted = sorted(dateArray) # Sort datetimes from earliest to latest

print "Grouping images taken within %s seconds of each other..." % timeDelta

# miniArray temporarily holds a group of datetimes before appending
# them to gifDates. First add the current datetime to miniArray, if
# the next date is within [timeDelta] seconds of the first datetime,
# then add it to miniArray. If it is not within [timeDelta] seconds,
# then check if miniArray has more than one object in it. If it does
# have for than one object, we can make a gif out of it, so append
# miniArray's current array to gifDates, and then clear it by
# setting the only object within miniArray as the current datetime.
# Lastly, if miniArray only has one object in it, clear it by
# setting the only object within miniArray as the current datetime.
miniArray = [dateSorted[0].strftime("%Y%m%d%H%M%S")]
for index, x in enumerate(dateSorted[1:]):
	if ((x - dateSorted[index - 1]).total_seconds() <= timeDelta):
		miniArray.append(x.strftime("%Y%m%d%H%M%S"))
	elif (len(miniArray) > 1):
		miniArray.append(x.strftime("%Y%m%d%H%M%S"))
		gifDates.append(miniArray)
		miniArray = [x.strftime("%Y%m%d%H%M%S")]
	else:
		miniArray = [x.strftime("%Y%m%d%H%M%S")]

print ("Converting image groups to gifs...")

images = [] # Group of images to create a gif out of
# Go through each index in gifDates and create a gif out of the
# images within each group
for index, x in enumerate(gifDates):
	# Resize each image in the group to be 750x500
	for y in x:
		img = Image.open(imgDic[y])
		img = img.resize((750,500))
		images.append(img);

	writeGif("%s%s.gif" % (gifName, index),images,duration=0.2,dither=50)
	images = [] # Clear images

print "Complete!"

