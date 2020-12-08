# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 18:53:29 2020

@author: Jasmine

For Bernard: You only need the bottom values: degree_left and degree_right
"""
import cv2
import math
import numpy as np

# read the input image
img_rot = cv2.imread("./images/double4.jpg")

#     *********************************    
#     *                               *
#     *   Detects Circles in Images   *
#     *                               *
#     *********************************

img = cv2.imread("./images/double4.jpg", cv2.IMREAD_COLOR) 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
output = img.copy()

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3))
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT,1,40,
                                    param1=50,param2=30,minRadius=295,maxRadius=300)

# Draw circles that are detected. 
if detected_circles is not None: 
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles))

    if detected_circles[0][0][0] < 1000:
        xl, yl, rl = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xr, yr, rr = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]
    else:
        xr, yr, rr = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xl, yl, rl = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]

        
    a, b, r = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
    # Draw the circumference of the circle. 
    cv2.circle(img_rot, (xr, yr), rr, (0, 0, 255), 5)
    cv2.circle(img_rot, (xl, yl), rl, (0, 0, 255), 5)

#     *********************************    
#     *                               *
#     *    Applies Filter on Image    *
#     *                               *
#     *********************************

img_rot_hsv = cv2.cvtColor(img_rot, cv2.COLOR_BGR2HSV)

# find HSV using BGR
blue = np.uint8([[[226,211,99]]])
#print(cv2.cvtColor(pink,cv2.COLOR_BGR2HSV))
blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

# define range of pink color in HSV
# (H - 10, 100, 100)
# (H + 10, 255, 255)
lower_blue = np.array([blue[0][0][0] - 10,100,100])
upper_blue = np.array([blue[0][0][0] + 10,255,255])

# Threshold the HSV image to get only pink colors
mask_rot_blue = cv2.inRange(img_rot_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and rotated image
res_rot_blue = cv2.bitwise_and(img_rot,img_rot, mask=mask_rot_blue)
res_rot_blue = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2RGB)

# make copys of the results to display them
filtered_rot_blue = res_rot_blue.copy()

#     *********************************    
#     *                               *
#     *    Finds Center of Shape      *
#     *                               *
#     *********************************

# Calculate the center of the shape after filter is applied
gray_rot = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2GRAY)
blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours_rot:
    # calculate moments for each contour
    M = cv2.moments(c)
    
    # calculate x,y coordinate of center
    if M["m00"] != 0:
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
    else:
     cX, cY = 0, 0
    if cX < 1000:
        tl = np.array([(cX - xl), -1*(cY - yl), 0])
    else:
        tr = np.array([(cX - xr), -1*(cY - yr), 0])


#     *********************************    
#     *                               *
#     *       Calculates Angle        *
#     *                               *
#     *********************************


omega = np.array([xl, yl, 1])
s = np.array([0, 1, 0])

y = np.dot(np.transpose(omega), np.cross(s,tl))
x = np.dot(s, tl)
theta = math.atan2(y, x)
degree_left = np.rad2deg(theta)
degree_left = '%1.0f' % (degree_left)

y = np.dot(np.transpose(omega), np.cross(s,tr))
x = np.dot(s, tr)

theta = math.atan2(y, x)
degree_right = np.rad2deg(theta)
degree_right = '%1.0f' % (degree_right)

# NOTE: Degrees: positive rotate counter-clockwise, negative rotate clockwise
print("degree left: ", degree_left)
print("degree right: " , degree_right)


