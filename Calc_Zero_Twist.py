# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:42:00 2020

@author: Jasmine Anica

This program finds the angle of a zero-pitch twist

Uses OpenCV functions to find best fit circle of the gears to set the origin of
each gear. Use a filter to find the "base" points on the gears and the "rotated"
points on the gears. The filter picks up on the blue tag positions in the base 
image and the rotated image. Using OpenCV functions, I can calculate the centor
of the filtered shapes. Take the difference of the points relative to thier 
origin and find the angles that way.

For Bernard: You only need the bottom values: degree_left and degree_right   
"""
import cv2
import math
import numpy as np

# read the input image
img_base = cv2.imread("./images/doublebase.jpg")
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
origin_l = []
origin_r = [] 
# Draw circles that are detected. 
if detected_circles is not None: 
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles))
    
    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
      
        # Draw the circumference of the circle. 
        cv2.circle(img, (a, b), r, (0, 255, 0), 5)
    
    
    if detected_circles[0][0][0] < 1000:
        xl, yl, rl = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xr, yr, rr = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]
    else:
        xr, yr, rr = detected_circles[0][0][0], detected_circles[0][0][1], detected_circles[0][0][2]
        xl, yl, rl = detected_circles[0][1][0], detected_circles[0][1][1], detected_circles[0][1][2]
    
    origin_l = np.array([xl, yl, 1])
    origin_r = np.array([xr, yr, 1])
        
    # Draw the circumference of the circle. 
    cv2.circle(img_rot, (xr, yr), rr, (0, 0, 255), 5)
    cv2.circle(img_rot, (xl, yl), rl, (0, 0, 255), 5)
    
#     *********************************    
#     *                               *
#     *    Applies Filter on Image    *
#     *                               *
#     *********************************

img_base_hsv = cv2.cvtColor(img_base, cv2.COLOR_BGR2HSV)

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
mask_base_blue = cv2.inRange(img_base_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and rotated image
res_base_blue = cv2.bitwise_and(img_base,img_base, mask=mask_base_blue)
res_base_blue = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2RGB)

################################################################################

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


#     *********************************    
#     *                               *
#     *    Finds Center of Shape      *
#     *                               *
#     *********************************

# Calculate the center of the shape after filter is applied
gray_base = cv2.cvtColor(res_base_blue, cv2.COLOR_BGR2GRAY)
blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

base_pt_l  = []
base_pt_r = []

for c in contours_base:
    # calculate moments for each contour
    M = cv2.moments(c)
    
    # calculate x,y coordinate of center
    if M["m00"] != 0:
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
    else:
     cX, cY = 0, 0
    cv2.circle(img_rot, (cX, cY), 5, (255, 255, 255), 10)
    cv2.putText(img_rot, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 3)
    #print("rot center:", cX, cY)
    t = np.array([(cX - a), -1*(cY - b), 0])
    if cX < 1000: #left side 
        base_pt_l = np.array([cX, cY, 1])
        #print("base_l ", base_pt_l)
    else: #right side
        base_pt_r = np.array([cX, cY, 1])
        #print("base_r ", base_pt_r)

# Calculate the center of the shape after filter is applied
gray_rot = cv2.cvtColor(res_rot_blue, cv2.COLOR_BGR2GRAY)
blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

rot_pt_l  = []
rot_pt_r = []

for c in contours_rot:
    # calculate moments for each contour
    M = cv2.moments(c)
    
    # calculate x,y coordinate of center
    if M["m00"] != 0:
     cX = int(M["m10"] / M["m00"])
     cY = int(M["m01"] / M["m00"])
    else:
     cX, cY = 0, 0
    cv2.circle(img_rot, (cX, cY), 5, (255, 255, 255), 10)
    cv2.putText(img_rot, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 3)
    #print("rot center:", cX, cY)
    if cX < 1000:
        rot_pt_l = np.array([cX, cY, 1])
    else:
        rot_pt_r = np.array([cX, cY, 1])

#     *********************************    
#     *                               *
#     *       Calculates Angle        *
#     *                               *
#     *********************************

omega = np.array([0, 0, 1])

u_pt_l = base_pt_l - origin_l
v_pt_l = rot_pt_l - origin_l

y = np.dot(np.transpose(omega), np.cross(u_pt_l, v_pt_l))
x = np.dot(u_pt_l, v_pt_l)
theta = math.atan2(y, x)
degree_left = np.rad2deg(theta)
degree_left = '%1.0f' % (degree_left)
print("degree left: ", degree_left)

u_pt_r = base_pt_r - origin_r
v_pt_r = rot_pt_r - origin_r

y = np.dot(np.transpose(omega), np.cross(u_pt_r, v_pt_r))
x = np.dot(u_pt_r, v_pt_r)
theta = math.atan2(y, x)
degree_right = np.rad2deg(theta)
degree_right = '%1.0f' % (degree_right)
print("degree right: ", degree_right)

