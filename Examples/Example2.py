# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 18:12:19 2020

@author: Jasmine
"""

import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

# read the input image
img_base = cv2.imread("./images/base.jpg")
img_rotated = cv2.imread("./images/rot266.jpg")

#     *********************************    
#     *                               *
#     *   Detects Circles in Images   *
#     *                               *
#     *********************************

img = cv2.imread("./images/base.jpg", cv2.IMREAD_COLOR) 
gray = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
output = img.copy()

# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 
  
# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 520, maxRadius = 550)


max_pt = [0, 0, 0]

# Draw circles that are detected. 
if detected_circles is not None: 
  
    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles))
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        if max_pt[2] < r:
            max_pt[0] = a
            max_pt[1] = b
            max_pt[2] = r
  
    a, b, r = max_pt[0], max_pt[1], max_pt[2]
    print("origin: ", a, b)
  
    # Draw the circumference of the circle. 
    cv2.circle(img, (a, b), r, (255, 0, 0), 2) 
  
    # Draw a small circle (of radius 1) to show the center. 
    cv2.circle(img, (a, b), 1, (255, 0, 0), 3)

#     *********************************    
#     *                               *
#     *    Applies Filter on Image    *
#     *                               *
#     *********************************

img_base_hsv = cv2.cvtColor(img_base, cv2.COLOR_BGR2HSV)
img_rot_hsv = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2HSV)


# find HSV using BGR
blue = np.uint8([[[138,76,16]]])
print(cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)) 

# define range of blue color in HSV
# (H - 10, 100, 100)
# (H + 10, 255, 255)
lower_blue = np.array([95,100,100])
upper_blue = np.array([115,255,255])

# Threshold the HSV image to get only blue colors
mask_base = cv2.inRange(img_base_hsv, lower_blue, upper_blue)
mask_rot = cv2.inRange(img_rot_hsv, lower_blue, upper_blue)

# Bitwise-AND mask and base image
res_base = cv2.bitwise_and(img_base,img_base, mask=mask_base)
res_base = cv2.cvtColor(res_base, cv2.COLOR_BGR2RGB)

# Bitwise-AND mask and rotated image
res_rot = cv2.bitwise_and(img_rotated,img_rotated, mask=mask_rot)
res_rot = cv2.cvtColor(res_rot, cv2.COLOR_BGR2RGB)

# make copys of the results to display them
filtered_base = res_base.copy()
filtered_rot = res_rot.copy()

cv2.putText(filtered_base, "Filtered Base", (500, 1600),cv2.FONT_HERSHEY_SIMPLEX, 4.5, (255, 255, 255), 5)
plt.imshow(filtered_base),plt.show()
cv2.putText(filtered_rot, "Filtered Rotated", (450, 1600),cv2.FONT_HERSHEY_SIMPLEX, 4.5, (255, 255, 255), 5)
plt.imshow(filtered_rot),plt.show()


#     *********************************    
#     *                               *
#     *    Finds Center of Shape      *
#     *                               *
#     *********************************

# Calculate the center of the shape after filter is applied
gray_base = cv2.cvtColor(res_base, cv2.COLOR_BGR2GRAY)
blurred_base = cv2.GaussianBlur(gray_base, (5, 5), 0)
thresh_base = cv2.threshold(blurred_base, 60, 255, cv2.THRESH_BINARY)[1]

gray_rot = cv2.cvtColor(res_rot, cv2.COLOR_BGR2GRAY)
blurred_rot = cv2.GaussianBlur(gray_rot, (5, 5), 0)
thresh_rot = cv2.threshold(blurred_rot, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the binary image
contours_base, hierarchy = cv2.findContours(thresh_base,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours_rot, hierarchy = cv2.findContours(thresh_rot,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# calculate moments for each contour
M = cv2.moments(contours_base[0])

# calculate x,y coordinate of center
if M["m00"] != 0:
 cX = int(M["m10"] / M["m00"])
 cY = int(M["m01"] / M["m00"])
else:
 cX, cY = 0, 0
cv2.circle(img_base, (cX, cY), 5, (255, 255, 255), 10)
cv2.putText(img_base, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 3)

# convert from BGR to RGB so we can plot using matplotlib
img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2RGB)
plt.imshow(img_base),plt.show()

img = cv2.arrowedLine(img, (a, b), (cX, cY), (0, 0, 255), 5)
print("base center:", cX, cY)
s = np.array([cX - a, -1*(cY - b), 0])

# calculate moments for each contour
M = cv2.moments(contours_rot[0])

# calculate x,y coordinate of center
if M["m00"] != 0:
 cX = int(M["m10"] / M["m00"])
 cY = int(M["m01"] / M["m00"])
else:
 cX, cY = 0, 0
cv2.circle(img_rotated, (cX, cY), 5, (255, 255, 255), 10)
cv2.putText(img_rotated, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 3)
# convert from BGR to RGB so we can plot using matplotlib
img_rotated = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2RGB)
plt.imshow(img_rotated),plt.show()
print("rot center:", cX, cY)
t = np.array([(cX - a), -1*(cY - b), 0])

img = cv2.arrowedLine(img, (a, b), (cX, cY), (0, 0, 255), 5)


#     *********************************    
#     *                               *
#     *       Calculates Angle        *
#     *                               *
#     *********************************

omega = np.array([0, 0, 1])
y = np.dot(np.transpose(omega), np.cross(s,t))
x = np.dot(s, t)

theta = math.atan2(y, x)
degree = np.rad2deg(theta)
degree = '%1.3f' % (degree)

cv2.putText(img, degree, (a, b + 100),cv2.FONT_HERSHEY_SIMPLEX, 3.5, (0, 0, 0), 3)
plt.imshow(img),plt.show()


