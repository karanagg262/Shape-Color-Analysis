#######################################################################################

# TEAM ID  :  eYRC#1029
# TEAM MEMBERS : KARAN AGGARWAL, SHIVAM MEHRA, ADYA SHAMBHAVI, SHWETA KUMARI

######################################################################################

#classes and subclasses to import
import cv2
import numpy as np
import os
import argparse
import imutils
import math
from os.path import join,isfile
filename = 'results_1029.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()

def detectShape(image, c, cX, cY, color, ll):
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)
	# CHECKING NO. OF VERTICES
	if len(approx) == 3:
		shape = "TRIANGLE"

	elif len(approx) == 4:

		# COMPUTE THE BOUNDING BOX OF CONTOUR AND USE THIS TO
		# COMPUTE THE ASPECT RATIO
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		rect_diagonal = math.sqrt(w * w + h * h)
		# COMPUTE THE MIN ENCLOSING CIRCLE TO FIND THE QUADRILATERAL SHAPE
		(x, y), radius = cv2.minEnclosingCircle(c)
		center = (int(x), int(y))

		radius = int(radius)
		diameter = 2 * radius
		error = diameter / rect_diagonal
		# A SQUARE WILL HAVE AN ASPECT RATIO THAT IS APPROXIMATELY
		# EQUAL TO ONE OF NOT THEN IT COULD BE RHOMBUS WHOSE DIAGONAL
		# IS EQUAL TO THE DIAMETER OF THE MINIMUM ENCLOSING CIRCLE
		# ELSE IT IS TRAPEZIUM

		if ar >= 0.95 and ar <= 1.05:
		    shape = 'SQUARE'

		elif error >= 0.9 and error <= 1.1:
		    shape = 'RHOMBUS'
		else:
		    shape = 'TRAPEZIUM'
	elif len(approx) == 5:
		shape = "PENTAGON"

	elif len(approx) == 6:
		shape = "HEXAGON"
		# OTHERWISE , WE ASSUME THE SHAPE IS CIRCLE
	else:
		shape = "CIRCLE"
	    
	cv2.putText(image, shape, (cX-25, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
	writecsv(color, shape, (cX,cY))
	ll.append([color+'-'+shape+'-'+str(cX)+'-'+str(cY)])

def main(path):
#####################################################################################################
    #Write your code here!!!
#####################################################################################################
	# LOAD IMAGE FILE
	image = cv2.imread(path)

	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	# CONVERT IN GRAYSCALE THEN BLURRED IT THEN FIND THRESHOLD
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
	# FIND CONTOURS AND DETECT SHAPE
	cnts = cv2.findContours(thresh, 1, 2)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]


	# ..........................................DETECTING COLOUR.............................................................

	# define range of green color in HSV
	lower = np.array([50, 50, 120])
	upper = np.array([70, 255, 255])
	shapemask = cv2.inRange(hsv, lower, upper)

	# define range of blue color in HSV
	lower_blue = np.array([110, 50, 50])
	upper_blue = np.array([130, 255, 255])
	blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# define range of red color in HSV
	lower_red = np.array([0, 50, 50])
	upper_red = np.array([10, 255, 255])
	red_mask = cv2.inRange(hsv, lower_red, upper_red)

	hsv, cnts, _ = cv2.findContours(shapemask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	hsv, cnts1, _ = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	hsv, cnts2, _ = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	ll = [path]
	for c in cnts:
	    M = cv2.moments(c)
	    cgX = int((M["m10"] / M["m00"]))
	    cgY = int((M["m01"] / M["m00"]))
	    cv2.putText(image, '('+str(cgX)+','+str(cgY)+')', (cgX-25, cgY+15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
	    cv2.putText(image, 'GREEN', (cgX - 20, cgY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	    detectShape(image, c, cgX, cgY, 'GREEN', ll)
	for c in cnts1:
	    M = cv2.moments(c)
	    cbX = int((M["m10"] / M["m00"]))
	    cbY = int((M["m01"] / M["m00"]))
	    cv2.putText(image, '('+str(cbX)+','+str(cbY)+')', (cbX-25, cbY+15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)  
	    cv2.putText(image, 'BLUE', (cbX - 20, cbY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	    detectShape(image, c, cbX, cbY, 'BLUE', ll)

	for c in cnts2:
	    M = cv2.moments(c)
	    crX = int((M["m10"] / M["m00"]))
	    crY = int((M["m01"] / M["m00"]))
	    font = cv2.FONT_HERSHEY_SIMPLEX
	    cv2.putText(image, '('+str(crX)+','+str(crY)+')', (crX-25, crY+15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)	    
            cv2.putText(image, 'RED', (crX - 25, crY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	    detectShape(image, c, crX, crY, 'RED', ll)

	cv2.imshow("image", image)
	cv2.imwrite( path[0:len(path)-4]+"output.png", image );
	cv2.waitKey(0)
	return ll


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles:
        #Open the csv to write in append mode
        filep = open('results_1029.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results_1029.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
