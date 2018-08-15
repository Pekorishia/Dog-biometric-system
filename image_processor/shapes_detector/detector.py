# coding: utf-8

from shapedetector import ShapeDetector
from copy import deepcopy
import argparse
import imutils
import pprint
import math
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",      required=True,
	help="path to the input image")
ap.add_argument("-oi", "--outImage",  required=True,
	help="path to the output image")
ap.add_argument("-of", "--outFile",   required=True,
	help="path to the output text file")
ap.add_argument("-id", "--label",   required=True,
	help="image identifier")
args = vars(ap.parse_args())

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

# find contours in the thresholded image 
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
	   cv2.CHAIN_APPROX_NONE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# and initialize the shape detector
sd = ShapeDetector()

# shapes, center and perimeter array
scp = []

# Start the shapes counters
triangle = 0
square = 0
rectangle = 0
pentagon = 0
unidentified = 0

# loop over the contours
for c in cnts:

	M = cv2.moments(c)

	if M["m00"] != 0 :
		# calculate the center point
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		
		shape, perimeter, area = sd.detect(c)

		# add shape, center and perimeter to the array
		scp.append([shape, (cX, cY), perimeter, area])		
 
	# draw the contour and the name of the shape on the image
	#cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# get the image border (the root of the contours tree)
imageContour = deepcopy(cnts[0])

# sort the scp and cnts arrays based on the perimeter value on a downwards order
scp.sort(key=lambda tup: tup[2], reverse=True)
cnts.sort(key=lambda s: len(s), reverse=True)

# store the position of the pad contour on the cnts sorted array
padBorder = 0

# equality checker
checker = True

# if both have the same length, then they might be equals
if len(cnts[0]) == len(imageContour):
	# compare if the border contour is equals to the first contour
	#	for every pixel (x,y) inside both
	for i in range(len(cnts[0])):  
		if imageContour[i][0][0] !=  cnts[0][i][0][0]:
			checker = False
			break

		if imageContour[i][0][1] !=  cnts[0][i][0][1]:
			checker = False
			break
else :
	checker = False

# if the largest perimeter contour is the image border
if checker:
	# then the pad contour is the second one
	padBorder = 1
else :
	padBorder = 0

# draw the pad contour
cv2.drawContours(image, cnts, padBorder, (0, 255, 0), 2)

# get the first element of the contours
# it will be the referential contour of the image
elem = scp[padBorder]

# create the array that will have the closest distance between the shapes and the 
# referential element
globaldist = {'triangle' : -1, 'square' : -1,'rectangle' : -1, 'pentagon' : -1,'unidentified' : -1}

# for each element, calculate the euclidian distance
for compelem in scp:
	if (compelem != elem):
		# calculate the euclidian distance based on the center point
		dX = (elem[1][0] - compelem[1][0])** 2
		dY = (elem[1][1] - compelem[1][1])** 2
		dist = math.sqrt(dX + dY) 
		
		# if the actual distance is smaller than the actual one
		# or it is the first value calculated
		if (dist < globaldist[compelem[0]] or globaldist[compelem[0]] == -1):
			# put the distance inside the element distance array
			globaldist[compelem[0]] = dist


# open a .txt file
file = open(args["outFile"], "w")

# write the representative vector
# vector format: perimeter, area, nearest triangle, nearest square, 
#				 nearest rectangle, nearest pentagon, nearest unidentified and label
file.write( str(elem[2]) + ',' + str(elem[3]) + ',' + str(globaldist["triangle"]) + "," + str(globaldist["square"]) + "," + str(globaldist["rectangle"]) + "," + str(globaldist["pentagon"]) + "," + str(globaldist["unidentified"]) + "," + str(args["label"]));

# close the .txt file
file.close() 

# save the output image
cv2.imwrite(args["outImage"], image)

