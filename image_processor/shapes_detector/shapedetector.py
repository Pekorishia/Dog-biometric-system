# import opencv2
import cv2
 
class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour 
		# with an epsilon of 4%
		shape = "unidentified"
		area = cv2.contourArea(c)
		peri = len(c)
		approx = cv2.approxPolyDP(c, 0.1 * cv2.arcLength(c,True), True)
		
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
 
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
 
		# otherwise, we can't assume the shape
		else:
			shape = "unidentified"
 
		# return the name of the shape
		return shape, peri, area

	
